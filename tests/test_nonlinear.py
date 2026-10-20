"""Independent spectral and estimator checks for the QuEST extension."""
import numpy as np
import pytest
from scipy.integrate import quad
from scipy.optimize import brentq
from mvrl._vendor.quest.core import quest, _forward
from mvrl._vendor.quest.gradient import quest_grad
from mvrl.nonlinear import nonlinear_covariance


@pytest.mark.parametrize('p,n', [(10,119), (49,119), (10,8)])
def test_isotropic_population_has_constant_shrunk_spectrum(p,n):
    lam,delta,_=quest(np.ones(p),n)
    np.testing.assert_allclose(delta,1,atol=2e-10)
    assert abs(lam.mean()-1)<6e-4
    assert np.count_nonzero(lam==0)==max(p-n,0)


def test_quantized_eigenvalues_against_independent_marchenko_pastur_integrals():
    p,n=10,119;c=p/n;lo=(1-np.sqrt(c))**2;hi=(1+np.sqrt(c))**2
    density=lambda x:np.sqrt(max(0,(hi-x)*(x-lo)))/(2*np.pi*c*x)
    cdf=lambda x:quad(density,lo,x,epsabs=1e-11)[0]
    cuts=[lo]+[brentq(lambda x:cdf(x)-i/p,lo,hi) for i in range(1,p)]+[hi]
    reference=np.array([p*quad(lambda x:x*density(x),a,b,epsabs=1e-11)[0]
                        for a,b in zip(cuts[:-1],cuts[1:])])
    np.testing.assert_allclose(quest(np.ones(p),n)[0],reference,atol=2e-4,rtol=0)


def test_stieltjes_equation_and_analytic_jacobian():
    tau=np.linspace(.5,3,10);n=119;ctx=_forward(tau,n)
    st=-1/ctx.sol.zxi;x=ctx.den.x
    residual=x-(-1/st+np.sum(tau[None,:]/(1+tau[None,:]*st[:,None]),axis=1)/n)
    assert abs(residual).max()<1e-9
    h=1e-5
    fd=np.column_stack([(quest(tau+np.eye(10)[i]*h,n)[0]-quest(tau-np.eye(10)[i]*h,n)[0])/(2*h)
                        for i in range(10)])
    np.testing.assert_allclose(quest_grad(tau,n),fd,atol=5e-7,rtol=2e-5)


def test_covariance_equivariance_scale_and_cache(tmp_path):
    x=np.random.default_rng(5).normal(size=(120,10))@np.diag(np.linspace(.1,2,10))
    q=np.linalg.qr(np.random.default_rng(1).normal(size=(10,10)))[0]
    v,info=nonlinear_covariance(x,tmp_path)
    v_cached,cached=nonlinear_covariance(x,tmp_path)
    np.testing.assert_array_equal(v,v_cached);assert info==cached
    np.testing.assert_allclose(nonlinear_covariance(x*3)[0],9*v,atol=1e-8,rtol=1e-7)
    np.testing.assert_allclose(nonlinear_covariance(x@q)[0],q.T@v@q,atol=1e-8,rtol=1e-7)
    np.testing.assert_allclose(nonlinear_covariance(x+2)[0],v,atol=1e-8,rtol=1e-7)
    assert np.linalg.eigvalsh(v).min()>0
    assert info['quest_normalized_mse']<=info['quest_initial_mse']+1e-12
    assert abs(np.mean(info['quest_population_eigenvalues'])-np.mean(info['quest_sample_eigenvalues']))<1e-10
    with pytest.raises(ValueError):nonlinear_covariance(np.ones((5,10)))
    with pytest.raises(ValueError):nonlinear_covariance(np.zeros((120,10)))
