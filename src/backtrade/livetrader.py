import backtrader as bt
from typing import NoReturn

from src.live.foobar import FooBar
import backtrader_ib_insync as ibnew



def live_trader() -> NoReturn:
    cerebro = bt.Cerebro()
    storekwargs = dict(
        host= 'localhost', port=7497,
        clientId=None,
        account=None,
        timeoffset=True,
        reconnect=3, timeout=3.0,
        notifyall=True,
        _debug=False,
    )
    ibstore = ibnew.IBStore(**storekwargs)
    broker = ibstore.getbroker()
    cerebro.setbroker(broker)


    ibdata = ibstore.getdata

    datakwargs = dict(
    timeframe= bt.TimeFrame.Seconds, compression=1,
    rtbar=False,
    qcheck=0.5,
    what=None,
    backfill_start=True, backfill=True,
    latethrough=True,
    tz=None,
    useRTH = False,
    hist_tzo = None,
    )

    data0 = ibdata(dataname='EUR.USD-CASH-IDEALPRO', **datakwargs)

    cerebro.resampledata(data0, timeframe=bt.TimeFrame.Seconds, compression=2)


    cerebro.addstrategy(FooBar)
    cerebro.run()
