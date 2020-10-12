
nVars = 10
beta_min = 0
beta_max = 10
batch_len = 50

model = 'linearModel'
model.p = nVars
model.sparsity = 1
#model.betas = runif(nVars, beta_min, beta_max)
model.betas = c(2, 2, 3, 3, 2, 1, 4, 5, 6, 2)
shrunkCoefs = sample(1:nVars, floor(nVars*max(0, 1 - model.sparsity)))
if (length(shrunkCoefs) > 1) model.betas = model.betas[shrunkCoefs] = 0
model.alpha = 0.1

linearPrediction <- function(vars)
    model.alpha + sum(model.betas*vars) 

data = matrix(0, batch_len, nVars + 1)
colnames(data) = c(paste(sep='', rep('x', nVars), 1:10), "y")

linearGeneration <- function(sigma = 0.1) {
    vars = runif(model.p, 0, 1)   
    y = model.alpha + sum(model.betas*vars) + rnorm(1, 0, sigma)
    return(c(vars, y))
}

for (i in 0:batch_len) {
    data[i, ] = linearGeneration()
}

write.csv(data, file="data/test.csv", row.names=F)