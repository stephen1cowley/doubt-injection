# 1 Introduction

## 1.1 Motivation

## 1.2 Technical Background

### 1.2.1 Large Language Models

### 1.2.2 Hallucination
- Popular definitions
- Expanding the definition

### 1.2.3 Effect of Prompt
- "The effects of this will be discussed later in section X"

### 1.2.4 Effect of Temperature
- "THis will be explored later"

### 1.2.5 Retrival-augmented Generation

### 1.2.6 Contrastive Decoding
- "Sections X will attempt to verify the results seen in the literature"

### 1.2.7 Chain-of-Thought


## 1.3 Objectives

# 2 Additive Context-aware Decoding to Address Issues with Contrastive Decoding

## 2.1 Theory

## 2.2 Experimental Setup

### 2.2.1 Datasets

### 2.2.2 Metrics
- Recall, EM

### 2.2.3 Models

## 2.3 Results and Discussion

### 2.3.1 Reproduction of CAD Results

### 2.3.2 Differences Across Papers

### 2.3.3 CAD-DoLa

### 2.3.4 Probability Simplex Visualisation

### 2.3.5 Additive CAD

# 3 Wider Exploration of Idea Space with Doubt Injection

## 3.1 Theory

## 3.2 Experimental Setup

### 3.2.1 Datasets

### 3.2.2 Metrics
- AVG@X

### 3.2.3 Evaluating Error (Beta distribution)
- Provided equal weighting of questions

### 3.2.4 Models
- Reference the DeepSeek paper with small background on where the model has come from.

### 3.2.5 Nucleus Setting (top-p)
- Equation

## 3.3 Results and Discussion

### 3.3.1 Motivating Results (the River Problem)

### 3.3.2 Exploration of Idea Space

### 3.3.3 Effect of Injection String

### 3.3.4 Effect of Injection Probability

### 3.3.5 Effect of Temperature

### 3.3.6 Performance on Alternative Datasets

# 4 Conclusions

## 4.1 Future Work
