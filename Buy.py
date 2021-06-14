import win32com.client


# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

# 주문 초기화
objTrade =  win32com.client.Dispatch("CpTrade.CpTdUtil")

initCheck = objTrade.TradeInit(0)

if (initCheck != 0):
    print("주문 초기화 실패")
    exit()


# 주식 매수 주문
acc = objTrade.AccountNumber[0] #계좌번호
accFlag = objTrade.GoodsList(acc, 1)  # 주식상품 구분
print(acc, accFlag[0])
objStockOrder = win32com.client.Dispatch("CpTrade.CpTd0311")
objStockOrder.SetInputValue(0, "2")   # 2: 매수
objStockOrder.SetInputValue(1, acc )   #  계좌번호
objStockOrder.SetInputValue(2, accFlag[0])   # 상품구분 - 주식 상품 중 첫번째
objStockOrder.SetInputValue(3, "A005930")   # 종목코드 - 필요한 종목으로 변경 필요
objStockOrder.SetInputValue(4, 10)   # 매수수량 - 요청 수량으로 변경 필요
objStockOrder.SetInputValue(5, 10000)   # 주문단가 - 필요한 가격으로 변경 필요
objStockOrder.SetInputValue(7, "0")   # 주문 조건 구분 코드, 0: 기본 1: IOC 2:FOK
objStockOrder.SetInputValue(8, "01")   # 주문호가 구분코드 - 01: 보통

# 매수 주문 요청
nRet = objStockOrder.BlockRequest()
if (nRet != 0) :
    print("주문요청 오류", nRet)
    # 0: 정상,  그 외 오류, 4: 주문요청제한 개수 초과
    exit()

rqStatus = objStockOrder.GetDibStatus()
errMsg = objStockOrder.GetDibMsg1()
if rqStatus != 0:
    print("주문 실패: ", rqStatus, errMsg)
    exit()
