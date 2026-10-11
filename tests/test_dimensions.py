"""Data-integrity and calibration checks for the added industry universes."""
import zipfile
import numpy as np
import pytest
from mvrl.historical import data,french_monthly,moments,solve_family,objective

@pytest.mark.parametrize('n',[10,30,49])
def test_dimension_data_complete_and_calibration(n):
    frame=data(n)
    assert frame.shape==(672,n+1)
    assert np.isfinite(frame.to_numpy()).all()
    # Two different market states, with a real lagged covariance and no future data.
    for t in (240,600):
        hist=frame.iloc[t-120:t,:-1].to_numpy()-frame.RF.iloc[t-120:t].to_numpy()[:,None]
        m,v=moments(hist);p=np.ones(n)/n
        ps,info=solve_family(m,v,5.,p,.001,['target','raw','penalty_only','joint'])
        assert np.linalg.norm(ps['joint']-ps['target'])<2e-5
        assert abs(objective(m,v,ps['joint'],5.,p,.001)-objective(m,v,ps['target'],5.,p,.001))<1e-8
        assert max(info['certificates'].values())<=2e-7

def test_date_filter_does_not_hide_in_window_missing_or_read_second_block(tmp_path):
    p=tmp_path/'sample.zip'
    with zipfile.ZipFile(p,'w') as z:
        z.writestr('sample.csv','Monthly\n,A,B\n196912,-99.99,1\n197001,1,2\n\n197001,99,99\n')
    f=french_monthly(p,'Monthly',197001,197012)
    np.testing.assert_allclose(f.to_numpy(),[[.01,.02]])
    with pytest.raises(ValueError,match='missing'):
        french_monthly(p,'Monthly',196912,197012)
    with pytest.raises(ValueError,match='no monthly block'):
        french_monthly(p,'Monthly',198001,198012)
