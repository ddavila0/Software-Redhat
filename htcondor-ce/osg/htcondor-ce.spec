
Name: htcondor-ce
Version: 0.5.3
Release: 1%{?dist}
Summary: A framework to run HTCondor as a CE

Group: Applications/System
License: Apache 2.0
URL: http://github.com/bbockelm/condor-ce

Source0: %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires:  condor
# This ought to pull in the HTCondor-CE specific version of the blahp
Requires: blahp
Requires: %{name}-client

Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts

%description
%{summary}

%package condor
Group: Applications/System
Summary: Default routes for submission to HTCondor

Requires: %{name} = %{version}-%{release}

%description condor
%{summary}

%package pbs
Group: Applications/System
Summary: Default routes for submission to PBS

Requires: %{name} = %{version}-%{release}
Requires: /usr/bin/grid-proxy-init
Requires: /usr/bin/voms-proxy-init

%description pbs
%{summary}

%package client
Group: Applications/System
Summary: Client-side tools for submission to HTCondor-CE

# Note the strange requirements (base package is not required!
# Point is to be able to submit jobs without installing the server.
Requires: condor
Requires: /usr/bin/grid-proxy-init
Requires: /usr/bin/voms-proxy-init

%description client
%{summary}

%prep
%setup -q -n condor-ce-%{version}

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Directories necessary for HTCondor-CE files
install -m 0755 -d -p $RPM_BUILD_ROOT/%{_localstatedir}/run/condor-ce
install -m 0755 -d -p $RPM_BUILD_ROOT/%{_localstatedir}/log/condor-ce
install -m 1777 -d -p $RPM_BUILD_ROOT/%{_localstatedir}/log/condor-ce/user
install -m 0755 -d -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/condor-ce
install -m 0755 -d -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/condor-ce/spool
install -m 0755 -d -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/condor-ce/execute
install -m 0755 -d -p $RPM_BUILD_ROOT/%{_localstatedir}/lock/condor-ce
install -m 1777 -d -p $RPM_BUILD_ROOT/%{_localstatedir}/lock/condor-ce/user
install -m 1777 -d -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/gratia/condorce_data

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add condor-ce

%preun
if [ $1 = 0 ]; then
  /sbin/service condor-ce stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del condor-ce
fi

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service condor-ce condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)

%{_bindir}/condor_ce_history
%{_bindir}/condor_ce_router_q

%{_datadir}/condor-ce/condor_ce_env_bootstrap
%{_datadir}/condor-ce/condor_ce_router_defaults

%{_initrddir}/condor-ce

%dir %{_sysconfdir}/condor-ce
%dir %{_sysconfdir}/condor-ce/config.d
%config %{_sysconfdir}/condor-ce/condor_config
%config %{_sysconfdir}/condor-ce/config.d/01-ce-auth.conf
%config %{_sysconfdir}/condor-ce/config.d/01-ce-router.conf
%config(noreplace) %{_sysconfdir}/condor-ce/condor_mapfile
%config(noreplace) %{_sysconfdir}/sysconfig/condor-ce

%attr(-,condor,condor) %dir %{_localstatedir}/run/condor-ce
%attr(-,condor,condor) %dir %{_localstatedir}/log/condor-ce
%attr(1777,condor,condor) %dir %{_localstatedir}/log/condor-ce/user
%attr(-,condor,condor) %dir %{_localstatedir}/lib/condor-ce
%attr(-,condor,condor) %dir %{_localstatedir}/lib/condor-ce/spool
%attr(-,condor,condor) %dir %{_localstatedir}/lib/condor-ce/execute
%attr(-,condor,condor) %dir %{_localstatedir}/lock/condor-ce
%attr(1777,condor,condor) %dir %{_localstatedir}/lock/condor-ce/user
%attr(1777,root,root) %dir %{_localstatedir}/lib/gratia/condorce_data

%files condor
%defattr(-,root,root,-)

%config %{_sysconfdir}/condor-ce/config.d/02-ce-condor.conf

%files pbs
%defattr(-,root,root,-)

%config %{_sysconfdir}/condor-ce/config.d/02-ce-pbs.conf

%files client
%{_bindir}/condor_ce_config_val
%{_bindir}/condor_ce_hold
%{_bindir}/condor_ce_q
%{_bindir}/condor_ce_qedit
%{_bindir}/condor_ce_rm
%{_bindir}/condor_ce_run
%{_bindir}/condor_ce_release
%{_bindir}/condor_ce_submit
%{_bindir}/condor_ce_reconfig
%{_bindir}/condor_ce_reschedule
%{_bindir}/condor_ce_status
%{_bindir}/condor_ce_version

%changelog
* Wed Dec 12 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5.3-1
- Implement the condor_ce_run helper utility.
- Split out client tools subpackage.

* Sat Jul 07 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5.2-1
- A second try at fixing the periodic hold expression.

* Fri Jul 06 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5.1-1
- Fix incorrect attribute name in the periodic hold expression.

* Tue Jun 19 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5-1
- Fix RPM deps and some small pbs_status tweaks.

* Thu Jun 14 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.4-1
- Tweak default route settings from limits hit in the scalability tests.
- Add support for RSV.

* Mon Jun 04 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.3-1
- Add support for Gratia.

* Thu May 31 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.2-1
- Release after a day of testing with PBS and HTCondor.


