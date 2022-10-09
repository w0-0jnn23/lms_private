import requests
from bs4 import BeautifulSoup

main_url = "https://lms.ksa.hs.kr"
login_url = main_url + "/Source/Include/login_ok.php"
docu_url_prefix = "https://lms.ksa.hs.kr/nboard.php?db=vod&mode=view&idx="
doce_url_suffix = "&page=1&ss=on&sc=&sn=&db=vod&scBCate=133"

session = requests.session()

login_info = {
    'user_id' : '22-096',
    'user_pwd' : 'test'
}

res = session.post(login_url, data = login_info)
res.raise_for_status()

def binary_search(find_name, find_date):
    start = 0
    end = 103094

    while start <= end:
        mid = (start + end) // 2
        output = search(str(mid))
        if not output:
            start -= 1
            continue
        print(str(mid)) # Test용
        if find_name in output[0] and find_date in output[1]:
            return mid
        elif find_date == output[1]:
            first_mid = mid
            while find_date == output[1]:
                mid += 1
                temp = search(str(mid))
                print(str(mid)) # Test용
                if temp:
                    output = temp
                    if find_name == output[0] and find_date == output[1]:
                        return mid
            mid = first_mid
            output = search(str(mid))
            while find_date == output[1]:
                mid -= 1
                temp = search(str(mid))
                print(str(mid)) # Test용
                if temp:
                    output = temp
                    if find_name == output[0] and find_date == output[1]:
                        return mid
            return None
        elif output[1] < find_date:
            start = mid + 1
        else:
            end = mid - 1
    return None
        
def search(id):
    res = session.get(make_link(id))
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    name = soup.find_all(attrs={'class':'title'})
    date = soup.find_all(attrs={'class':'blue01'})
    
    if not name or not date:
        return None
    
    date = get_date(date)
    
    return name[0].get_text(), date

def get_date(date):
    date = date[0].get_text()
    for i in range(len(date)):
        if date[i] == "록" and date[i+1] == "일":
            date = date[i+4:i+8] + date[i+9:i+11] + date[i+12:i+14]
            return date
    return None

def make_link(id):
    return docu_url_prefix + str(id) + doce_url_suffix

find_name = input("찾을 게시글의 이름을 입력하세요: ")
find_date = input("찾을 게시글의 날짜를 입력하세요(예: 20200101): ")

output = binary_search(find_name, find_date)

if output:
    print(make_link(output))
else:
    print("찾는 게시글이 없습니다.")