"""Controlled bounded short/borrow example; not a crypto execution simulator."""
import numpy as np
from scipy.optimize import minimize, LinearConstraint, linprog


def financing_cost(w, prev, turnover=.001, borrow=.002, short=.0005):
    return float(turnover*np.abs(w-prev).sum()+borrow*max(w.sum()-1,0)+short*np.maximum(-w,0).sum())


def solve_financing(m, hessian, prev, turnover=.001, borrow=.002, short=.0005):
    n=len(m);size=3*n+1
    # Variables w, absolute trade z, absolute holdings q, positive borrowing h.
    rows=[];rhs=[]
    for i in range(n):
        r=np.zeros(size);r[i]=1;r[n+i]=-1;rows.append(r);rhs.append(prev[i])
        r=np.zeros(size);r[i]=-1;r[n+i]=-1;rows.append(r);rhs.append(-prev[i])
        r=np.zeros(size);r[i]=1;r[2*n+i]=-1;rows.append(r);rhs.append(0)
        r=np.zeros(size);r[i]=-1;r[2*n+i]=-1;rows.append(r);rhs.append(0)
    r=np.zeros(size);r[:n]=1;r[-1]=-1;rows.append(r);rhs.append(1)
    r=np.zeros(size);r[2*n:3*n]=1;rows.append(r);rhs.append(1.6)
    r=np.zeros(size);r[:n]=1;rows.append(r);rhs.append(1.5)
    rows.append(-r);rhs.append(0)
    B=np.array(rows);b=np.array(rhs)
    bounds=[(-.5,.8)]*n+[(0,2)]*n+[(0,.8)]*n+[(0,.5)]
    linear=np.r_[-m-short/2,np.full(n,turnover),np.full(n,short/2),borrow]
    def f(x):return x[:n]@hessian@x[:n]+linear@x
    def grad(x):return linear+np.r_[2*hessian@x[:n],np.zeros(2*n+1)]
    x0=np.r_[prev,np.zeros(n),abs(prev),max(prev.sum()-1,0)]
    r=minimize(lambda x:1000*f(x),x0,jac=lambda x:1000*grad(x),bounds=bounds,
        constraints=LinearConstraint(B,-np.inf,b),method='SLSQP',options={'ftol':1e-11,'maxiter':1000})
    if np.max(B@r.x-b)>1e-7:raise RuntimeError('infeasible financing solution')
    lp=linprog(grad(r.x),A_ub=B,b_ub=b,bounds=bounds,method='highs')
    if not lp.success:raise RuntimeError(lp.message)
    certificate=max(0.,float(grad(r.x)@(r.x-lp.x)))
    if certificate>2e-7:raise RuntimeError(f'financing certificate {certificate}')
    return r.x[:n],certificate
