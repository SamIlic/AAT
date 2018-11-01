
#install.packages('depmixS4')
#install.packages('quantmod')
library('depmixS4')
library('quantmod')
set.seed(1)

# Create the parameters for the bull and bear market returns distributions
Nk_lower <- 50
Nk_upper <- 150
bull_mean <- 0.1
bull_var <- 0.1
bear_mean <- -0.05
bear_var <- 0.2

### The Nk values are randomly chosen:
# Create the list of durations (in days) for each regime
days <- replicate(5, sample(Nk_lower:Nk_upper, 1))

### The returns for each kth period are randomly drawn:
# Create the various bull and bear markets returns
market_bull_1 <- rnorm( days[1], bull_mean, bull_var ) 
market_bear_2 <- rnorm( days[2], bear_mean, bear_var ) 
market_bull_3 <- rnorm( days[3], bull_mean, bull_var ) 
market_bear_4 <- rnorm( days[4], bear_mean, bear_var ) 
market_bull_5 <- rnorm( days[5], bull_mean, bull_var )



### The R code for creating the true regime states (either 1 for bullish or 2 for bearish) 
#       and final list of returns is given by the following:
# Create the list of true regime states and full returns list
true_regimes <- c( rep(1,days[1]), rep(2,days[2]), rep(1,days[3]),rep(2,days[4]), rep(1,days[5]))
returns      <- c( market_bull_1, market_bear_2, market_bull_3, market_bear_4, market_bull_5)

# plot the returns: which shows clear changes in mean and variance between the regime switches
plot(returns, type="l", xlab='Days', ylab="Returns")

# Fit & Specify the Hidden Markov Model via the Expectation Maximization algorithm
# Create and fit the Hidden Markov Model
hmm <- depmix(returns ~ 1, family = gaussian(), nstates = 2,
                  data=data.frame(returns=returns))
hmmfit <- fit(hmm, verbose = FALSE)


# Output both the true regimes and the
# posterior probabilities of the regimes
post_probs <- posterior(hmmfit)
layout(1:2)
plot(post_probs$state, type='s', main='True Regimes',
       xlab='', ylab='Regime')
matplot(post_probs[,-1], type='l',
          main='Regime Posterior Probabilities',
          ylab='Probability')
legend(x='topright', c('Bull','Bear'), fill=1:2, bty='n')


# Obtain S&P500 data from 2004 onwards and 
# create the returns stream from this
getSymbols( "^GSPC", from="2004-01-01" )
gspcRets = diff( log( Cl( GSPC ) ) )
returns = as.numeric(gspcRets)
plot(gspcRets)


# Fit a Hidden Markov Model with 2-states
# to the S&P500 returns stream
hmm <- depmix(returns ~ 1, family = gaussian(), nstates = 2,
                  data=data.frame(returns=returns))
hmmfit <- fit(hmm, verbose = FALSE)
post_probs <- posterior(hmmfit)

# Plot the returns stream and the posterior
# probabilities of the separate regimes
layout(1:2)
plot(returns, type='l', main='Regime Detection', xlab='', ylab='Returns') 
matplot(post_probs[,-1], type='l', main='Regime Posterior Probabilities', ylab='Probability')
legend(x='bottomleft', c('Regime #1','Regime #2'), fill=1:2, bty='n')


# Fit a Hidden Markov Model with 3-states
# to the S&P500 returns stream
hmm <- depmix(returns ~ 1, family = gaussian(), nstates = 3,
                  data=data.frame(returns=returns))
hmmfit <- fit(hmm, verbose = FALSE)
post_probs <- posterior(hmmfit)

# Plot the returns stream and the posterior
# probabilities of the separate regimes
layout(1:2)
plot(returns, type='l', main='Regime Detection',
       xlab='', ylab='Returns')
matplot(post_probs[,-1], type='l',
          main='Regime Posterior Probabilities',
          ylab='Probability')
legend(x='bottomleft', c('Regime #1','Regime #2', 'Regime #3'),
                            fill=1:3, bty='n')






