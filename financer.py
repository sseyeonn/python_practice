import FinanceDataReader as fdr # 무료 주식 web api 가져옴
from flask import Flask, request, jsonify
from flask_cors import CORS # 앱으로 접속하기 위함

app = Flask(__name__)
CORS(app)

# 접속할 수 있는 url decorate
# 주소 : http://127.0.0.1/stock?page=1&ppv=20 웹브라우저 접속만
@app.route('/stock', methods=['GET'])

def get_all_stock():
    
    req_page = request.args.get('page') # page : 1 -> String
    if isinstance(req_page, str):
        req_page = int(req_page)
        
    if req_page is None:
        req_page = 1
        
    if req_page < 1:
        return jsonify({'error' : 'page should be greater than 0'}), 400 # 정상 : 200
    

    view_count = request.args.get('ppv')
    if isinstance(view_count, str):
        view_count = int(view_count)
        
    if view_count is None:
        view_count = 20
        
    if view_count < 1:
        return jsonify({'error' : 'page should be greater than 0'}), 400 # 정상 : 200
    
    
    start_idx = (req_page - 1) * view_count
    end_idx = start_idx + view_count
    
    try:
        stock = fdr.StockListing('KRX') # 한국거래소 상장종목 전체 (like 엑셀표)
        count = stock.shape[0] # 반환받는 값을 몇행 몇열인지 변환하고 Row : 전체 종목 개수 구함 
        
        all_stock = []
        for i in range(start_idx, end_idx):
            stock_data = stock.iloc[i].to_dict() # pandas : iloc 행 번호 -> dic 형태 (예: 종목명:삼전, 현재가:70,000)
            all_stock.append(stock_data) # 20개까지 추가
            
        output = {}
        output['total_count'] = count
        pages = count // view_count # 전체 페이지 정보 (F-END : 페이징 처리 수월)
        output['total_page'] = pages if count % view_count == 0 else pages + 1
        output['data'] = all_stock
        
        return jsonify(output), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500        
        
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8070)