import pdfplumber
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
PDF_PATH = os.getenv("PDF_PATH")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# ================= 1. PDF 파싱 =================
def parse_pdf(pdf_path):
    transactions = []
    print(f"📂 PDF 읽는 중: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"❌ 파일을 찾을 수 없습니다.")
        return []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text: full_text += text + "\n"
            
            lines = full_text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # 날짜 검색 (YYYY.MM.DD)
                # 날짜와 시간이 붙어있는 경우(예: 2026.01.2607:36:44)를 대비해 전처리
                line_fixed = re.sub(r'(\d{4}\.\d{2}\.\d{2})(\d{2}:\d{2}:\d{2})', r'\1 \2', line)
                
                date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', line_fixed)
                if not date_match: continue

                try:
                    date_str = date_match.group(1)
                    time_match = re.search(r'(\d{2}:\d{2}:\d{2})', line_fixed)
                    time_str = time_match.group(1) if time_match else "00:00:00"
                    
                    # 저장용 전체 시간 (KST +09:00 명시)
                    date_iso = f"{date_str.replace('.', '-')}T{time_str}+09:00"
                    
                    # 금액 추출
                    parts = line_fixed.split()
                    numeric_parts = []
                    for p in parts:
                        # 콤마 제거
                        clean_p = p.replace(',', '')
                        # 음수 부호(-) 처리: -1234 처럼 숫자 앞에 붙은 경우만 허용하거나
                        # 단순히 -와 숫자로만 구성되었는지 확인
                        # isdigit()은 음수를 인식 못하므로 lstrip('-') 사용
                        if clean_p.lstrip('-').isdigit():
                            numeric_parts.append(int(clean_p))
                    
                    if not numeric_parts: continue
                    amount = numeric_parts[0]
                    balance = numeric_parts[1] if len(numeric_parts) > 1 else 0
                    
                    # 구분 (텍스트 OR 금액 부호 기반)
                    if "입금" in line_fixed:
                        kind = "입금"
                    elif "출금" in line_fixed:
                        kind = "출금"
                    else:
                        # 한글 깨짐 대비: 금액 부호로 판단
                        if amount < 0:
                            kind = "출금"
                        else:
                            kind = "입금"
                    
                    # 메모 정제
                    clean_memo = line_fixed
                    clean_memo = re.sub(r'\d{4}\.\d{2}\.\d{2}', '', clean_memo)
                    clean_memo = re.sub(r'\d{2}:\d{2}:\d{2}', '', clean_memo)
                    clean_memo = re.sub(r'\b-?\d{1,3}(,\d{3})*\b', '', clean_memo) # 콤마 포함 숫자, 음수 포함 제거
                    clean_memo = re.sub(r'\b-?\d+\b', '', clean_memo) # 일반 숫자, 음수 포함 제거
                    clean_memo = clean_memo.replace("입금", "").replace("출금", "")
                    clean_memo = clean_memo.replace('"', '').replace("'", "").strip()
                    if not clean_memo: clean_memo = "내용없음"

                    transactions.append({
                        "date": date_iso,
                        "kind": kind,
                        "amount": amount,
                        "balance": balance,
                        "memo": clean_memo,
                        "sub_kind": clean_memo.split()[-1] if clean_memo else ""
                    })
                except:
                    continue

    except Exception as e:
        print(f"❌ 오류: {e}")
        return []
    
    # 최신순 정렬
    transactions.sort(key=lambda x: x['date'])
    return transactions

# ================= 2. 중복 확인 (노션 데이터 형식 때문에 분 단위까지만 비교) =================
def get_existing_keys():
    print("🔍 노션 데이터 조회 중")
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    existing_keys = set()
    has_more = True
    next_cursor = None

    while has_more:
        payload = {"page_size": 100}
        if next_cursor: payload["start_cursor"] = next_cursor
        
        try:
            res = requests.post(url, headers=headers, json=payload)
            data = res.json()
            if "results" not in data: break

            for result in data["results"]:
                props = result["properties"]
                try:
                    # 날짜를 16자리(분 단위)까지만 자름
                    # "2026-01-12T06:10:00..." -> "2026-01-12T06:10"
                    raw_date = props["거래일시"]["date"]["start"]
                    clean_date = raw_date[:16] 
                    
                    clean_amount = int(props["거래금액"]["number"])
                    
                    title_list = props["구분"]["title"]
                    clean_kind = title_list[0]["text"]["content"] if title_list else ""
                    
                    # 키 생성: 날짜(분)_금액_구분
                    unique_key = f"{clean_date}_{clean_amount}_{clean_kind}"
                    existing_keys.add(unique_key)
                    
                except (KeyError, IndexError, TypeError):
                    continue
            
            has_more = data.get("has_more", False)
            next_cursor = data.get("next_cursor")
        except:
            break
            
    return existing_keys

# ================= 3. 업로드 =================
def upload_to_notion(data):
    url = "https://api.notion.com/v1/pages"
    
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "구분": { "title": [{"text": {"content": data["kind"]}}] },
            "거래일시": { "date": {"start": data["date"]} },
            "거래금액": { "number": data["amount"] },
            "거래 후 잔액": { "number": data["balance"] },
            "거래내용(메모)": { "rich_text": [{"text": {"content": data["memo"]}}] },
            "거래구분": { "rich_text": [{"text": {"content": data["sub_kind"]}}] }
        }
    }
    
    requests.post(url, headers=headers, json=payload)
    print(f"✅ [저장] {data['date']} | {data['amount']:,}원 | {data['memo']}")

# ================= 실행 =================
if __name__ == "__main__":
    new_data = parse_pdf(PDF_PATH)
    
    if new_data:
        existing_keys = get_existing_keys()
        
        print("\n🚀 동기화 시작...")
        count = 0
        for tr in new_data:
            # PDF 데이터도 16자리(분 단위)까지만 잘라서 키 생성
            # tr['date']는 "2026-01-12T06:10:39" 형식이므로 [:16] 하면 "2026-01-12T06:10"이 됨
            current_key = f"{tr['date'][:16]}_{tr['amount']}_{tr['kind']}"
            
            if current_key in existing_keys:
                print(f"   [중복] 건너뜀: {tr['date']} ({tr['amount']}원)")
                continue
            
            upload_to_notion(tr)
            count += 1
            
        print(f"\n✨ 완료! {count}건이 새로 저장되었습니다.")
    else:
        print("⚠️ 데이터 없음")