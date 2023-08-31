# Parakeet Roadmap

## What we want to have

- Data representation should be relatively transferable between in-memory data and large, out-of-memory data.
- There should be friendly way to *implement* new analyses so that it is easy to replicate the basics of Cyclops functionality.
- Guarantees that the user can only create analyses that make sense, if possible: it should be impossible to calculate the IV of a continuous variable.
- It should be possible to compose results and analyses.

### Data Representation and Computation Engines

- [ ] [Polars!](https://www.pola.rs/)
- [ ] SQL
  - [ ] BigQuery?
  - [ ] [sqlx](https://docs.rs/sqlx/latest/sqlx/)
  - [ ] [PRQL](https://prql-lang.org/)
- [ ] Pandas?

### Core Concepts!

- [ ] Analysis specifications
  - Should we bring analysis concepts to the core? I have a feeling the core was quite empty without them... but maybe that's good.
- [ ] Analysis configurations
  - Should only contain information regarding *how to compute* an analysis.
  - Any information related to how to display results should be postponed
- [ ] Computation Engine
- [ ] Dataset
- [ ] Observations?
  - It would be nice to have a way to represent whether data comes from continuous or discrete distributions directly, without having to do so within the context of an analysis. This could be optional and have an inference mechanism, such as inferring from the data types or from cardinality.
  - A counter-argument is that this is typically not necessary: you may very well use the information directly just as numbers etc. It could be possible, but would make it harder to enforce validation strategies.
  - Some knowledge of the distribution (or at least of the universe of symbols) is helpful in simplifying computation. 

### Analyses!

- [ ] Discrete x Discrete
  - [ ] Measures of Distribution
    - [ ] Frequency Tables
    - [ ] Histogram
    - [ ] Stratified Analysis
    - [ ] Stratified Stability over Time
- [ ] Discrete x Continuous
  - [ ] Average
  - [ ] Std Dev
  - [ ] TODO: what else goes here?
- [ ] Continuous x Discrete
  - [ ] Bivariate Continuous Summary: a score vs a binary or categorical target
    - AUC
    - Gini
    - KS
    - Lorenz Curve
    - ...
  - [ ] TODO: 
- [ ] TODO: Continuous x Continuous
- [ ] TODO: Tweedie

Correlacao
Describe
State Transitions
Waterfall
ECDF
Frequency + Histogram

## The essentials: v0 target

My goal for a first usable version is that it should be possible to calculate some statistics that we're typically looking for.
In general, I prefer to start with discrete data.
Ideally, it should be possible to make a nice EDA notebook/script showing off the capabilities of the library. 

### What should be avoided

- Visuals. It takes a long time to make beautiful presentations, and it is typically non-transferable. In this sense, we still had a very active discussion on how to better make our visualizations easy to export or to update automatically.
- Complex, new stuff such as the bivariate-continuous-summary. Focus on what is known. 
- Statistical tests: it is hard to make good statistical tests, especially if you have to understand how they work first.

### v0 Roadmap

- [ ] Dataset
  - [ ] Basic interface definition (trait?)
  - [ ] Basic Polars implementation without any optimization
- [ ] Core
  - [ ] Definition of some basic analyses
    - [ ] Frequency Table
    - [ ] Stratified Analysis
  - [ ] Computation engine: bare bones + polars implementation
- [ ] Analyses
  - [ ] Discrete x Discrete
    - [ ] Frequency
    - [ ] Histogram
    - [ ] Base Strata


### Example

engine = <Backend>Engine(...)
dataset = <Backend>Dataset(...)
bad_rate_over_time = engine.stability(dataset, bad_rate, [var1, var2])
bad_rate_over_time.display() # Generate standard view

population = engine.waterfall(
    dataset,
    [
        Total(name='PF'),
        Delta(name='Has Credit Limit', dim='credit_limit_gt_0'),
        Total(name='Eligible'),
    ]
)
population.display() -> HTML
...

Engine -> Client BQ, Connector, etc
Stats -> Definicao da analise (schema minimo), Visualization
Impl -> Como calcular analise X -> Stats