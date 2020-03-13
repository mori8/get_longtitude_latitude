import urllib.request
import urllib.parse
import json

# 본인의 Application key 값을 입력해 줍니다.
client_id = ""  # your client id
client_secret = ""  # your client secret

# 주소 정보를 포함한 json 파일을 불러옵니다.
with open("selective_clinic.json", "r", encoding='UTF-8') as f:
    data = json.load(f)

for d in data:
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    query = "?query=" + urllib.parse.quote(d["주소 "])  # d의 key value로 주소가 담긴 key를 넘겨줍니다.

    url_query = url + query

    # Open API 검색 요청 개체 설정, 네이버 개발자센터의 정책 때문에 꼭 추가해야 합니다.
    request = urllib.request.Request(url_query)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)

    # 검색 요청 및 처리
    response = urllib.request.urlopen(request)
    res_code = response.getcode()

    if res_code == 200:
        # 정상적으로 실행된 경우
        response_json = json.loads(response.read())
        d['x'] = response_json["addresses"][0]["x"]
        d['y'] = response_json["addresses"][0]["y"]
    else:
        # 에러가 발생한 경우
        print("An error has occurred; error code:", res_code)

# 위도, 경도 정보를 추가한 새로운 data 파일 저장
print(json.dumps(data, indent="\t", ensure_ascii=False))
with open('selective_clinic_with_x_y.json', 'w', encoding='utf-8') as make_file:
    make_file.write(json.dumps(data, indent='\t', ensure_ascii=False))
