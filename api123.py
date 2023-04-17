import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/leaf-info',methods=['POST'])
def leaf_info():
    if request.method == 'POST':
        data = request.get_json()
        scientific_name=data['scientific_name']
    url1 = f'https://www.google.com/search?q={scientific_name}'
    url2 = f'https://www.google.com/search?q=medicinal+properties+of+{scientific_name}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response1 = requests.get(url1,headers=headers)
    response2 = requests.get(url2, headers=headers)
    soup1 = BeautifulSoup(response1.text, 'html.parser')
    soup2= BeautifulSoup(response2.text, 'html.parser')
    # search_result = soup2.find('div', class_='g')
    common_name = soup1.find('span', class_='yKMVIe').text.strip()
    
    desc = soup1.find('div', class_='kno-rdesc')
    description = desc.find('span').text.strip()
    medicinal_properties = soup2.find('span', class_='hgKElc').text.strip()
    data = {
        'common_name': common_name,
        'description': description,
        'medicinal_properties': medicinal_properties
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=5000)
