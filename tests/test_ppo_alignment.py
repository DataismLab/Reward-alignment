"""Checks of the sampled PPO intervention, independent of performance claims."""
import numpy as np
import pytest
pytest.importorskip('gymnasium')
from mvrl.ppo_alignment import ConditionalEnv, fitted_continuation, train_ppo


def test_sample_continuation_against_enumerated_paths():
    r=np.array([[[.1,.3],[-.2,.2]], [[.4,.0],[.1,-.1]]])
    j=np.array([[[0,1],[1,0]], [[0,1],[1,0]]])
    u=np.array([[.7,-.2],[.3,.8]])
    c=fitted_continuation(r,j,u,1.02)
    for z in range(2):
        paths=[1.02*r[0,z,i]*u[0,z]+r[1,j[0,z,i],k]*u[1,j[0,z,i]]
               for i in range(2) for k in range(2)]
        assert c[0,z]==pytest.approx(np.mean(paths))
    np.testing.assert_array_equal(c[-1],0.)


@pytest.mark.parametrize('method',['myopic','continuation'])
def test_reward_pair_and_reset_reproducibility(method):
    rng=np.random.default_rng(18)
    r=rng.uniform(-.2,.2,(3,2,40));j=rng.integers(2,size=r.shape)
    e=ConditionalEnv(r,j,2.,1.03,method,7)
    e.c=rng.normal(size=(4,2))
    obs,_=e.reset(seed=19)
    replay=np.random.default_rng(19);z=int(replay.integers(2))
    saved=[]
    for t in range(3):
        i,k=replay.integers(40,size=2);H=1.03**(2-t);u=.6
        dc=e.c[t+1,j[t,z,i]]-e.c[t+1,j[t,z,k]] if method=='continuation' else 0.
        want=H*(r[t,z,i]+r[t,z,k])*u/2-(H*(r[t,z,i]-r[t,z,k])*u+dc)**2
        step=e.step([u]);saved.append(step)
        assert step[1]==pytest.approx(want)
        assert step[2]==(t==2) and not step[3]
        assert e.observation_space.contains(step[0])
        z=int(j[t,z,i])
    np.testing.assert_array_equal(e.reset(seed=19)[0],obs)
    # A state-constant critic offset must leave every paired reward unchanged.
    e.c+=np.arange(4)[:,None]*100
    for previous in saved:
        current=e.step([.6])
        np.testing.assert_array_equal(current[0],previous[0])
        assert current[1]==pytest.approx(previous[1],abs=1e-12)


def test_ppo_smoke_has_bounded_finite_policy_and_sample_critic():
    pytest.importorskip('stable_baselines3')
    rng=np.random.default_rng(31)
    r=rng.uniform(-.2,.2,(3,2,64));j=rng.integers(2,size=r.shape)
    u,c,_=train_ppo(r,j,1.,1.02,'continuation',seed=1,steps=512)
    assert u.shape==(3,2) and np.isfinite(u).all() and np.max(np.abs(u))<=3
    np.testing.assert_allclose(c,fitted_continuation(r,j,u,1.02))
