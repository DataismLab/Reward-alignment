# Industry-dimension extension — fixed before inspecting outcomes, 2026-10-01

Motivation: DeMiguel, Garlappi and Uppal (2009) makes estimation error and the equal-weight hurdle central to portfolio evaluation. Increasing N alone cannot establish investment superiority. Extend the ten-industry audit to the public French 30- and 49-industry value-weighted monthly portfolios.

Keep original settings: estimation data January 1970–December 2025; evaluation January 1990–December 2025 (432 decisions); 120 lagged observations; phi=5; first-order L1 turnover cost 0.001; covariance 10% diagonal shrinkage; simplex constraints; equal initial holdings. Use existing August 2026 vintage RF and August 2026 vintage industry files. Reject missing data within the specified period; exclude pre-1970 missing industries rather than imputing them.

Run target, raw second moment, unconstrained scalar, risk-only, joint, equal weight and minimum variance. This extends the dimension check, not the full RL reward comparison: MVPI/log comparators stay in the original ten-industry primary study. Save all 432 x 7 decisions for each added universe. Preserve previous primary data/results.

Report common-state Euclidean distance and fitted objective gap, plus own-state realised MV, Sharpe, turnover and paired 12-month circular-block bootstrap intervals (1000 repetitions, seed 8128) for joint against raw and equal weight. Compare outcomes within each universe. N/L is 0.0833, 0.25, 0.4083; independent mean/covariance entries number 65, 495 and 1274. These counts describe estimation burden, not independent parameters or statistical degrees of freedom. The classifications differ, so this is a robustness check across universes, not a causal experiment changing N alone and not an N>L stress test.

Verification: complete dates, finite data, no missing in-window sentinels, lag-only moments, feasible common/own allocations, certified quadratic solutions, independently recomputed realised returns and fitted gaps, exact-calibration identity within numerical tolerances. No hyperparameter selection from the extension's realised outcomes.
