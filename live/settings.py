BUS_NUMBER = int(input('ავტობუსის ნომერი: '))

LIVE_URLS = [
    f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/buses?routeNumber={BUS_NUMBER}&forward=0',
    f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/buses?routeNumber={BUS_NUMBER}&forward=1'
]
STOP_URLS = [
    f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/routeStops?routeNumber={BUS_NUMBER}&forward=0',
    f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/routeStops?routeNumber={BUS_NUMBER}&forward=1'
]

DIRECTION = {
    0: 'არა მთავარი',
    1: 'მთავარი'
}

secret_token = 'sk.eyJ1IjoibmFtcGVyIiwiYSI6ImNqemxsMDR4djAzZDkzanBiMGNheGs4dHMifQ.VNRhf1JGDRPL-x0rry3Ngg'


def formatter(sp: str, extend: int) -> int:
    # sp to be changed from 3 to 1 , and from 1 to 3 
    return (len(sp) + 2)%4 + extend
