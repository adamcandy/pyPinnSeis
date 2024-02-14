#!/usr/bin/env python


#### Parameters
### Physical
nx=100#number of nodes along x axis. used here to remove the specfem's absorbing regions from PINN's computational domain
nz=100

n_abs=10#  # of nodes for absorbing B.C in both directions from specfem
n_absx=n_abs# nodes from left side of the domain
n_absz=n_abs#the top boundary is not absorbing


ax_spec=1.5#domain size in specfem before removing absorbing regions
az_spec=0.5
xsf=1.3#x location of all the seismometers in specfem

dx=ax_spec/nx
dz=az_spec/nz
rho=1.0
ax=xsf-n_absx*dx#dimension of the domain in the x direction for PINNs training. Note
#we just need to remove the thickness of the absorbing B.C on the left since 
#xsf is (must be) smaller than where the right side absorbing B.C starts 
az=az_spec-n_absz*dz#dimension of the domain in the z direction
t_m=0.5#total time for PDE training.
t_st=0.1#this is when we take the first I.C from specfem
t_s=0.5#total time series used from the seismograms

s_spec=5e-5#specfem time stepsize
t01=2000*s_spec#initial disp. input at this time from spec
t02=2300*s_spec#sec "initial" disp. input at this time from spec instead of enforcing initial velocity
t_la=5000*s_spec# test data for comparing specfem and trained PINNs



n_event=1# number of seismic events
n_seis=20#number of input seismometers from SPECFEM; if events have different 
#numbers of seismometers, you have to change the lines containing n_seis accordingly
z0_s=az# z location of the first seismometer from SPECFEM in PINN's refrence frame.Here it must
# be in km while in SPECFEM it's in meters. Note here we assume seismometers are
# NOT all on the surface and they are on a vertical line with the same x; the first 
#seismometers is at the surface and the next one goes deeper

zl_s=0.06-n_absz*dz# z location of the last seismometer at depth. this doesn't have 
#to be zero and can be higher especially if you have absorbing B.C at the bottom, change
#this accordingly based on what you used from specfem 



Lx=3;#this is for scaling the wavespeed in the PDE via saling x coordinate
Lz=3;#this is for scaling the wavespeed in the PDE via scaling z coordinate
