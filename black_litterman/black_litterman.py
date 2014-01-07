# Black-Litterman example code for python (bl_idz.py)
# Copyright (c) Jay Walters, blacklitterman.org, 2012.
#
# Redistribution and use in source and binary forms, 
# with or without modification, are permitted provided 
# that the following conditions are met:
#
# Redistributions of source code must retain the above 
# copyright notice, this list of conditions and the following 
# disclaimer.
# 
# Redistributions in binary form must reproduce the above 
# copyright notice, this list of conditions and the following 
# disclaimer in the documentation and/or other materials 
# provided with the distribution.
#  
# Neither the name of blacklitterman.org nor the names of its
# contributors may be used to endorse or promote products 
# derived from this software without specific prior written
# permission.
#  
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND 
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR 
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH 
# DAMAGE.
#
# This program uses the examples from the paper
# "A STEP-BY-STEP GUIDE TO THE BLACK-LITTERMAN MODEL, Incorporating
# user-specified confidence levels" by Thomas Idzorek. You can find
# a copy of this paper at the following url.
#   http://faculty.fuqua.duke.edu/~charvey/Teaching/BA453_2006/Idzorek_onBL.pdf
#
# For more details on the Black-Litterman model you can also view
# "The BlackLitterman Model: A Detailed Exploration", by this author
# at the following url.
#     http://papers.ssrn.com/sol3/papers.cfm?abstract_id=1314585
#

import numpy as np
from scipy import linalg

# blacklitterman
#   This function performs the Black-Litterman blending of the prior
#   and the views into a new posterior estimate of the returns using the
#   alternate reference model as shown in Idzorek's paper.
# Inputs
#   delta  - Risk tolerance from the equilibrium portfolio
#   weq    - Weights of the assets in the equilibrium portfolio
#   sigma  - Prior covariance matrix
#   tau    - Coefficiet of uncertainty in the prior estimate of the mean (pi)
#   P      - Pick matrix for the view(s)
#   Q      - Vector of view returns
#   Omega  - Matrix of variance of the views (diagonal)
# Outputs
#   Er     - Posterior estimate of the mean returns
#   w      - Unconstrained weights computed given the Posterior estimates
#            of the mean and covariance of returns.
#   lambda - A measure of the impact of each view on the posterior estimates.
#
def altblacklitterman(delta, weq, sigma, tau, P, Q, Omega):
    # Reverse optimize and back out the equilibrium returns
    # This is formula (12) page 6.
    pi = weq.dot(sigma * delta)
    # We use tau * sigma many places so just compute it once
    ts = tau * sigma
    # Compute posterior estimate of the mean
    # This is a simplified version of formula (8) on page 4.
    middle = linalg.inv(np.dot(np.dot(P,ts),P.T) + Omega)
    er = np.expand_dims(pi,axis=0).T + np.dot(np.dot(np.dot(ts,P.T),middle),(Q - np.expand_dims(np.dot(P,pi.T),axis=1)))
    # Compute posterior estimate of the mean
    # This is a simplified version of formula (8) on page 4.
    middle = linalg.inv(np.dot(np.dot(P,ts),P.T) + Omega)
    er = np.expand_dims(pi,axis=0).T + np.dot(np.dot(np.dot(ts,P.T),middle),(Q - np.expand_dims(np.dot(P,pi.T),axis=1)))
    # Compute posterior estimate of the uncertainty in the mean
    # This is a simplified and combined version of formulas (9) and (15)
    # Compute posterior weights based on uncertainty in mean
    w = er.T.dot(linalg.inv(delta * sigma)).T
    # Compute lambda value
    # We solve for lambda from formula (17) page 7, rather than formula (18)
    # just because it is less to type, and we've already computed w*.
    lmbda = np.dot(linalg.pinv(P).T,(w.T * (1 + tau) - weq).T)
    return [er, w, lmbda]

# idz_omega
#   This function computes the Black-Litterman parameters Omega from
#   an Idzorek confidence.
# Inputs
#   conf   - Idzorek confidence specified as a decimal (50% as 0.50)
#   P      - Pick matrix for the view
#   Sigma  - Prior covariance matrix
# Outputs
#   omega  - Black-Litterman uncertainty/confidence parameter
#
def bl_omega(conf, P, Sigma):
    alpha = (1 - conf) / conf
    omega = alpha * np.dot(np.dot(P,Sigma),P.T)
    return omega

# Function to display the results of a black-litterman shrinkage
# Inputs
#   title - Displayed at top of output
#   assets    - List of assets
#   res       - List of results structures from the bl function
#
def display(title,assets,res):
    er = res[0]
    w = res[1]
    lmbda = res[2]
    print('\n' + title)
    line = 'Country\t\t'
    for p in range(len(P)):
        line = line + 'P' + str(p) + '\t'
    line = line + 'mu\tw*'
    print(line)

    i = 0;
    for x in assets:
        line = '{0}\t'.format(x)
        for j in range(len(P.T[i])):
            line = line + '{0:.1f}\t'.format(100*P.T[i][j])

        line = line + '{0:.3f}\t{1:.3f}'.format(100*er[i][0],100*w[i][0])
        print(line)
        i = i + 1

    line = 'q\t\t'
    i = 0
    for q in Q:
        line = line + '{0:.2f}\t'.format(100*q[0])
        i = i + 1
    print(line)

    line = 'omega/tau\t'
    i = 0
    for o in Omega:
        line = line + '{0:.5f}\t'.format(o[i]/tau)
        i = i + 1
    print(line)

    line = 'lambda\t\t'
    i = 0
    for l in lmbda:
        line = line + '{0:.5f}\t'.format(l[0])
        i = i + 1
    print(line)



# Take the values from Idzorek, 2005.
weq = np.array([.193400,.261300,.120900,.120900,.013400,.013400,.241800,.034900 ])
V = np.array([[.001005,.001328,-.000579,-.000675,.000121,.000128,-.000445,-.000437],
    [.001328,.007277,-.001307,-.000610,-.002237,-.000989,.001442,-.001535],
    [-.000579,-.001307,.059852,.027588,.063497,.023036,.032967,.048039],
    [-.000675,-.000610,.027588,.029609,.026572,.021465,.020697,.029854],
    [.000121,-.002237,.063497,.026572,.102488,.042744,.039443,.065994],
    [.000128,-.000989,.023036,.021465,.042744,.032056,.019881,.032235],
    [-.000445,.001442,.032967,.020697,.039443,.019881,.028355,.035064],
    [-.000437,-.001535,.048039,.029854,.065994,.032235,.035064,.079958]])
refPi = np.array([0.0008,0.0067,0.0641,0.0408,0.0743,0.0370,0.0480,0.0660])
assets={'US Bonds  ','Intl Bonds','US Lg Grth','US Lg Value','US Sm Grth',
'US Sm Value','Intl Dev Eq','Intl Emg Eq'}

# Risk aversion of the market 
delta = 3.07

# Coefficient of uncertainty in the prior estimate of the mean
# from footnote (8) on page 11
tau = 0.025
tauV = tau * V

# Define view 1
# International Developed Equity will have an excess return of 5.25%
# with a confidence of 25%.
P1 = np.array([0,0,0,0,0,0,1,0])
Q1 = np.array([0.0525])
conf1 = 0.25

# Define view 2
# International Bonds will outperform US Bonds by 0.0025 with a
# confidence of 50%.
P2 = np.array([-1,1,0,0,0,0,0,0])
Q2 = np.array([0.0025])
conf2 = 0.50

# Define View 3
# US Large and Small Growth will outperform US Large and Small Value
# by 0.02 with a confidence of 65%.
P3 = np.array([0,0,0.90,-0.90,0.10,-0.10,0,0])
Q3 = np.array([0.02])
conf3 = 0.65

# Combine the views
P=np.array([P1,P2,P3])
Q=np.array([Q1,Q2,Q3]);

# Apply the views with simple Omega
Omega = np.dot(np.dot(P,tauV),P.T)
res = altblacklitterman(delta, weq, V, tau, P, Q, Omega)
display('Simple Omega',assets,res)

# Now apply the views using the Idzorek's method
tauV = tau * V
Omega = np.array([[bl_omega(conf1, P1, tauV), 0, 0],[0, bl_omega(conf2, P2, tauV), 0],[0, 0, bl_omega(conf3, P3, tauV)]])
res = altblacklitterman(delta, weq, V, tau, P, Q, Omega)
display('Idzorek Method',assets,res)
