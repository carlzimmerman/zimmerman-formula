import sympy as s,json,sys
from pathlib import Path
u,V,N,a,X0,rho0=s.symbols('u V N a X0 rho0',positive=True)
ud,Vd,Nd,Qd=s.symbols('ud Vd Nd Qd',real=True)
X=u**2/2;P=-rho0+a*(X-X0)**2/2;PX=a*(X-X0);K=PX+a*u**2
rho=u**2*PX-P;q=V*PX*u;E=V*rho;H=N*E
out=[]
def eq(n,x,y=0):
 r=s.factor(x-y);assert r==0,(n,r);out.append(n)
eq('actual_charge_velocity_derivative',s.diff(q,u),V*K)
eq('actual_density_velocity_derivative',s.diff(rho,u),u*K)
qdot=s.diff(q,u)*ud+s.diff(q,V)*Vd
Edot=s.diff(E,u)*ud+s.diff(E,V)*Vd
eq('off_shell_energy_charge_work',Edot,-P*Vd+u*qdot)
udsource=(Qd-Vd*PX*u)/(V*K)
eq('source_energy_work_identity',Edot.subs(ud,udsource),-P*Vd+u*Qd)
eq('source_free_volume_work',Edot.subs(ud,udsource.subs(Qd,0)),-P*Vd)
Hdot=s.diff(H,N)*Nd+s.diff(H,u)*ud+s.diff(H,V)*Vd
eq('canonical_lapse_and_volume_work',Hdot.subs(ud,udsource),Nd*E+N*(-P*Vd+u*Qd))
uvac=s.sqrt(2*X0)
eq('vacuum_charge',q.subs(u,uvac))
eq('vacuum_density_constant',rho.subs(u,uvac),rho0)
eq('vacuum_pressure',P.subs(u,uvac),-rho0)
eq('vacuum_extensive_energy',E.subs(u,uvac),V*rho0)
eq('vacuum_volume_work',(-P*Vd).subs(u,uvac),rho0*Vd)
eq('vacuum_velocity_unchanged_in_sourcefree_volumechange',udsource.subs(Qd,0).subs(u,uvac))
# d>0 maps to positive sound/current/kinetic; expansion drains buffer density.
d,Hv=s.symbols('d Hv',positive=True)
subs={u:s.sqrt(2*(X0+d)),Vd:Hv*V}
rdot=s.diff(rho,u)*udsource.subs(Qd,0)
eq('source_free_density_equation',rdot,-Vd/V*(rho+P))
eq('buffer_density_adiabatic_rate',rdot.subs(subs,simultaneous=True),-2*a*Hv*(X0+d)*d)
xdot=u*udsource.subs(Qd,0)
eq('buffer_displacement_rate',xdot.subs(subs,simultaneous=True),-2*Hv*(X0+d)*d/(2*X0+3*d))
assert s.simplify(xdot.subs(subs,simultaneous=True)).is_negative is True;out.append('buffer_displacement_decreases_in_expansion')
assert s.simplify(rdot.subs(subs,simultaneous=True)).is_negative is True;out.append('buffer_density_decreases_in_expansion')
eq('charge_density_inverse_volume',s.diff(q/V,u)*udsource.subs(Qd,0),-Vd*q/V**2)
# Small positivebuffer conservedq implies densityexcess dilutedatfirstorder.
eq('small_buffer_charge',s.limit((PX*u).subs(u,s.sqrt(2*(X0+d)))/d,d,0,dir='+'),a*s.sqrt(2*X0))
eq('small_buffer_energy',s.limit((rho.subs(u,s.sqrt(2*(X0+d)))-rho0)/d,d,0,dir='+'),2*a*X0)
eq('small_buffer_pressure',s.limit((P.subs(u,s.sqrt(2*(X0+d)))+rho0)/d,d,0,dir='+'))
# Staticvolume sourcefree cannot gainintegratedphysicalenergy by lapsealone.
eq('static_volume_physical_energy_constant',Edot.subs(ud,udsource).subs({Vd:0,Qd:0}))
eq('static_volume_canonical_lapse_reference_work',Hdot.subs(ud,udsource).subs({Vd:0,Qd:0}),Nd*E)
result={'all_passed':True,'count':len(out),'checks':out,'scope':'Existing C2 on arbitrary prescribed homogeneous lapse/volume; not live metric dynamics or proof of cold-to-DE transfer'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
