###############################################################################
###############################################################################
##
##  Copyright (C) 2004-2010 Red Hat, Inc.  All rights reserved.
##
##  This copyrighted material is made available to anyone wishing to use,
##  modify, copy, or redistribute it subject to the terms and conditions
##  of the GNU General Public License v.2.
##
###############################################################################
###############################################################################

# keep around ready for later user
## global alphatag rc4

# When downloading directly from Mercurial, it will automatically add this prefix
# Invoking 'hg archive' wont but you can add one with:
#  hg archive -t tgz -p "Cluster-Resource-Agents-" -r $altversion $altversion.tar.gz
%global altprefix Cluster-Resource-Agents-
%global altversion a7c0f35916bf

Name: resource-agents
Summary: Open Source HA Resource Agents for Red Hat Cluster
Version: 3.0.12
Release: 15%{?alphatag:.%{alphatag}}%{?dist}.1
License: GPLv2+ and LGPLv2+
Group: System Environment/Base
URL: http://sources.redhat.com/cluster/wiki/
Source0: https://fedorahosted.org/releases/c/l/cluster/%{name}-%{version}.tar.bz2
Source1: http://hg.linux-ha.org/agents/archive/%{altversion}.tar.bz2
Source2: ocf-tester.8
Source3: sfex_init.8
Patch0: drop_support_for_drbd_and_smb.patch
Patch1: halvm_lvm_agent_incorrectly_reports_vg_in_volume_list.patch
Patch2: resolve_incorrect_default_for_vm_agent.patch
Patch3: add_missing_resource_docs.patch
Patch4: clean_up_recursion_and_documentation.patch
Patch5: Make_vm.sh_use_stop_start_timeouts.patch
Patch6: fix_incorrect_link_resolution_in_fs_lib.patch
Patch7: add_nfsv4_support.patch
Patch8: install_nfsv4_agent.patch
Patch9: fix_migration_mapping_behavior.patch
Patch10: add_rhevm_status_program.patch
Patch11: sigquit_if_sigterm_was_not_fast_enough.patch
Patch12: resource_agent_tomcat-6.patch
Patch13: tomcat-6_change_build_system.patch
Patch14: fs-lib_allow_other_values_for_yes.patch
Patch15: drop_tomcat_5_from_build.patch
Patch16: psql_does_not_work_correctly_with_netmask.patch
Patch17: fix_utility_to_obtain_data_from_ccs_tool.patch

## Runtime deps
# system tools shared by several agents
Requires: /bin/bash /bin/grep /bin/sed /bin/gawk
Requires: /bin/ps /usr/bin/pkill /bin/hostname
Requires: /sbin/fuser
Requires: /sbin/findfs /bin/mount

# fs.sh
Requires: /sbin/quotaon /sbin/quotacheck
Requires: /sbin/fsck
Requires: /sbin/fsck.ext2 /sbin/fsck.ext3 /sbin/fsck.ext4

# ip.sh
Requires: /sbin/ip /usr/sbin/ethtool
Requires: /sbin/rdisc /usr/sbin/arping /bin/ping /bin/ping6

# lvm.sh
Requires: /sbin/lvm

# netfs.sh
Requires: /sbin/mount.nfs /sbin/mount.nfs4 /sbin/mount.cifs
Requires: /usr/sbin/rpc.nfsd /sbin/rpc.statd /usr/sbin/rpc.mountd

## Setup/build bits
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Build dependencies
BuildRequires: cluster-glue-libs-devel glib2-devel
BuildRequires: automake autoconf pkgconfig
BuildRequires: libxslt docbook-style-xsl
BuildRequires: python perl

ExclusiveArch: i686 x86_64

%description
A set of scripts to interface with several services to operate in a
High Availability environment for both Pacemaker and rgmanager
service managers.

%if 0%{?rhel} == 0
%package -n ldirectord
Summary:          Monitor daemon for maintaining high availability resources
Group:            System Environment/Daemons
Requires:         ipvsadm
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig

# We were originally ldirectord, then renamed with a heartbeat- prefix.
# Upstream maintainer wishes to use no prefix, which is consistent with 
# how it is packaged for other distributions
Provides:  ldirectord = 3.0.0-15
Obsoletes: ldirectord < 3.0.0-15
Provides:  heartbeat-ldirectord = 3.0.0-15
Obsoletes: heartbeat-ldirectord < 3.0.0-15

# removed for now until it's in Fedora
#Requires:  perl(Net::IMAP::Simple::SSL)

%description -n ldirectord
ldirectord is a stand-alone daemon to monitor services of real 
for virtual services provided by The Linux Virtual Server
(http://www.linuxvirtualserver.org/). It is simple to install 
and works with the heartbeat code (http://www.linux-ha.org/).
%endif

# we inherit configure from cluster project. Configure it for vars we need.
# building from source directly without those parameters will NOT work.
# See http://www.redhat.com/archives/cluster-devel/2009-February/msg00003.html
%prep
%setup -q -n %{name}-%{version} -a 1
%patch0 -p1 -b .drop_support_for_drbd_and_smb
%patch1 -p1 -b .halvm_lvm_agent_incorrectly_reports_vg_in_volume_list
%patch2 -p1 -b .resolve_incorrect_default_for_vm_agent
%patch3 -p1 -b .add_missing_resource_docs
%patch4 -p1 -b .clean_up_recursion_and_documentation
%patch5 -p1 -b .Make_vm.sh_use_stop_start_timeouts
%patch6 -p1 -b .fix_incorrect_link_resolution_in_fs_lib
%patch7 -p1 -b .add_nfsv4_support
%patch8 -p1 -b .install_nfsv4_agent
%patch9 -p1 -b .fix_migration_mapping_behavior
%patch10 -p1 -b .add_rhevm_status_program
%patch11 -p1 -b .sigquit_if_sigterm_was_not_fast_enough
%patch12 -p1 -b .resource_agent_tomcat-6
%patch13 -p1 -b .tomcat-6_change_build_system
%patch14 -p1 -b .fs-lib_allow_other_values_for_yes
%patch15 -p1 -b .drop_tomcat_5_from_build
%patch16 -p1 -b .psql_does_not_work_correctly_with_netmask
%patch17 -p1 -b .fix_utility_to_obtain_data_from_ccs_tool

# prepare rgmanager RAs
%{_configure} \
  --sbindir=%{_sbindir} \
  --initddir=%{_sysconfdir}/rc.d/init.d \
  --libdir=%{_libdir} \
  --without_fence_agents \
  --disable_kernel_check

# prepare pacemaker RAs
cd %{altprefix}%{altversion}
./autogen.sh
%{configure} --enable-fatal-warnings=no --with-rsctmpdir=%{_var}/run/heartbeat/rsctmp

%build
##CFLAGS="$(echo '%{optflags}')" make %{_smp_mflags}
# %{_smp_mflags} is broken from upstream and unrequired for this project.
CFLAGS="$(echo '%{optflags}')" make -C rgmanager/src/resources
make -C %{altprefix}%{altversion} %{_smp_mflags}

%install
rm -rf %{buildroot}
make -C rgmanager/src/resources install DESTDIR=%{buildroot}
make -C %{altprefix}%{altversion} install DESTDIR=%{buildroot}

# tree fixup
cp $RPM_SOURCE_DIR/ocf-tester.8 $RPM_SOURCE_DIR/sfex_init.8 %{buildroot}/%{_mandir}/man8/

rm %{buildroot}/%{_libdir}/heartbeat/ocf-*
find %{buildroot} -type f -name '.ocf-*' -exec chmod 644 {} \;
find %{buildroot} -type f -name 'ocf-*' -exec chmod 644 {} \;
find %{buildroot} -type f -name '*.dtd' -exec chmod 644 {} \;
chmod 755 %{buildroot}/%{_sbindir}/ocf-tester
chmod 755 %{buildroot}/%{_datadir}/cluster/ocf-shellfuncs

%if 0%{?rhel} != 0
# ldirectord isn't included on RHEL
find %{buildroot} -name 'ldirectord.*' -exec rm -f {} \;
find %{buildroot} -name 'ldirectord' -exec rm -f {} \;
%endif

# Strange location, remove until we can confirm
rm -f %{buildroot}%{_libdir}/heartbeat/tickle_tcp

# Test harness, worth creating a devel package for?
rm -rf %{buildroot}%{_datadir}/resource-agents/ocft
rm -f  %{buildroot}%{_sbindir}/ocft

# symlink to allow pacemaker to use rgmanager RAs
cd %{buildroot}/usr/lib/ocf/resource.d/ && \
 ln -sf %{_datadir}/cluster/ redhat

%clean
rm -rf %{buildroot}

%if 0%{?rhel} == 0
%post -n ldirectord
/sbin/chkconfig --add ldirectord

%postun -n ldirectord -p /sbin/ldconfig

%preun -n ldirectord
/sbin/chkconfig --del ldirectord
%endif

%files
%defattr(-,root,root,-)
%doc doc/COPYING.* doc/COPYRIGHT doc/README.licence
%doc %{altprefix}%{altversion}/AUTHORS
%{_datadir}/cluster
%{_sbindir}/rhev-check.sh

%dir /usr/lib/ocf
%dir /usr/lib/ocf/resource.d
/usr/lib/ocf/resource.d/heartbeat
/usr/lib/ocf/resource.d/redhat
%{_sbindir}/ocf-tester
%{_sbindir}/sfex_init

%dir %{_datadir}/resource-agents
%doc %{_datadir}/resource-agents/ra-api-1.dtd
%{_mandir}/man7/*.7*
%{_mandir}/man8/*.8*

%dir %{_sysconfdir}/ha.d
%{_sysconfdir}/ha.d/shellfuncs

%dir %{_libdir}/heartbeat
%{_libdir}/heartbeat/findif
%{_libdir}/heartbeat/send_arp  
%{_libdir}/heartbeat/sfex_daemon
%{_includedir}/heartbeat/agent_config.h

%if 0%{?rhel} == 0
%files -n ldirectord
%defattr(-,root,root,-)
%doc %{altprefix}%{altversion}/COPYING 
%doc %{altprefix}%{altversion}/ldirectord/ldirectord.cf
%{_sbindir}/ldirectord
%config(noreplace) %{_sysconfdir}/logrotate.d/ldirectord
%{_sysconfdir}/init.d/ldirectord
%{_sysconfdir}/ha.d/resource.d/ldirectord
%{_mandir}/man8/ldirectord.8*
/usr/lib/ocf/resource.d/heartbeat/ldirectord
%endif

%changelog
* Tue Oct 05 2010 Lon Hohberger <lhh@redhat.com> - Version: 3.0.12-15.el6_0.1
- resource-agents: fix utility to obtain data from ccs_tool
  (fix_utility_to_obtain_data_from_ccs_tool.patch)
  Resolves: rhbz#640190

* Wed Jul 21 2010 Marek Grac <mgrac@redhat.com> - 3.0.12-15
- postgresql RA does not work correctly with netmask
  (psql_does_not_work_correctly_with_netmask.patch)
  Resolves: rhbz#614457

* Tue Jul 20 2010 Lon Hohberger <lhh@redhat.com> - 3.0.12-14
- resource-agents: Drop tomcat-5 from build
  (drop_tomcat_5_from_build.patch)
  Resolves: rhbz#593721

* Wed Jul 14 2010 Lon Hohberger <lhh@redhat.com> - 3.0.12-13
- Allow other values for "yes" in fs-lib when unmounting
  file systems
  (fs-lib_allow_other_values_for_yes.patch)
  Resolves: rhbz#614421

* Wed Jul 14 2010 Marek Grac <mgrac@redhat.com> - 3.0.12-12
- postgres RA will fail to stop gracefully if there 
  is active client connected
  (sigquit_if_sigterm_was_not_fast_enough.patch)
  Resolves: rhbz#612165
- new RA for tomcat6
  (resource_agent_tomcat-6.patch)
  (tomcat-6_change_build_system.patch)
  Resolves: rhbz#593721

* Mon Jul 12 2010 Lon Hohberger <lhh@redhat.com> - 3.0.12-10
- Fix changelog for 3.0.12-9 date
- Add RHEVM status program
  (add_rhevm_status_program.patch)
  Resolves: rhbz#609497

* Fri Jul 09 2010 Lon Hohberger <lhh@redhat.com> - 3.0.12-9
- Add NFSv4 server support
  (add_nfsv4_support.patch)
  (install_nfsv4_agent.patch)
  Resolves: rhbz#595547
- Fix migration mapping behavior
  (fix_migration_mapping_behavior.patch)
  Resolves: rhbz#596918

* Wed Jun 30 2010 Lon Hohberger <lhh@redhat.com> - 3.0.12-8
- Make fs-lib resolve links before checking for block devices
  (fix_incorrect_link_resolution_in_fs_lib.patch)
  Resolves: rhbz#609579

* Wed Jun 30 2010 Lon Hohberger <lhh@redhat.com> - 3.0.12-7
- Make vm.sh honor start and stop timeouts
  (Make_vm.sh_use_stop_start_timeouts.patch)
  Resolves: rhbz#606754

* Fri Jun 25 2010 Lon Hohberger <lhh@redhat.com> - 3.0.12-6
- Add missing documentation for resource agents
  (add_missing_resource_docs.patch)
- Clean up recursion in scheman output and documentation
  (clean_up_recursion_and_documentation.patch)
  Resolves: rhbz#606470

* Thu Jun  3 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.12-5
- Fix incorrect default for VM.sh agent
  (resolve_incorrect_default_for_vm_agent.patch)
  Resolves: rhbz#599643

* Fri May 28 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.12-4
- Add missing man pages
  (Add Source2: ocf-tester.8 and Source3: sfex_init.8)
  Resolves: rhbz#594332

* Wed May 19 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.12-3
- Do not package ldirectord on RHEL
  Resolves: rhbz#577264

* Wed May 19 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.12-2
- Drop Requires on xfsprogs since package moved to another channel
  Resolves: rhbz#593433
- Fix HALVM: lvm agent incorrectly reports vg is in volume_list
  (halvm_lvm_agent_incorrectly_reports_vg_in_volume_list.patch)
  Resolves: rhvz#593108

* Wed May 12 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.12-1
- Rebase on top of new upstream bug fix only release:
  * drop all bug fix patches.
  * refresh patches with official SHA1 git commits from RHEL6
    upstream branch:
    - drop_support_for_drbd_and_smb.patch
  * Addresses the follwing issues:
    from 3.0.12 release:
  Resolves: rhbz#582754, rhbz#582753, rhbz#585217, rhbz#583789
  * Rebase:
  Resolves: rhbz#582353
- Stop build on ppc and ppc64.
  Resolves: rhbz#590997
- Switch to file based Requires.
  Also address several other problems related to missing runtime
  components in different agents.
  With the current Requires: set, we guarantee all basic functionalities
  out of the box for lvm/fs/clusterfs/netfs/networking.
  Resolves: rhbz#584800
- New pacemaker agents upstream release
  * Patched build process to correctly generate ldirectord man page
  + High: pgsql: properly implement pghost parameter
  + High: RA: mysql: fix syntax error
  + High: SAPInstance RA: do not rely on op target rc when monitoring clones (lf#2371)
  + High: set the HA_RSCTMP directory to /var/run/resource-agents (lf#2378)
  + High: RA: vmware: fix set_environment() invocation (LF 2342)
  + High: RA: vmware: update to version 0.2
  + Medium: IPaddr/IPaddr2: add a description of the assumption in meta-data
  + Medium: IPaddr: return the correct code if interface delete failed
  + Medium: nfsserver: rpc.statd as the notify cmd does not work with -v (thanks to Carl Lewis)
  + Medium: oracle: reduce output from sqlplus to the last line for queries (bnc#567815)
  + Medium: pgsql: implement "config" parameter
  + Medium: RA: iSCSITarget: follow changed IET access policy
  + Medium: Filesystem: prefer /proc/mounts to /etc/mtab for non-bind mounts (lf#2388)
  + Medium: IPaddr2: don't bring the interface down on stop (thanks to Lars Ellenberg)
  + Medium: IPsrcaddr: modify the interface route (lf#2367)
  + Medium: ldirectord: Allow multiple email addresses (LF 2168)
  + Medium: ldirectord: fix setting defaults for configfile and ldirectord (lf#2328)
  + Medium: meta-data: improve timeouts in most resource agents
  + Medium: nfsserver: use default values (lf#2321)
  + Medium: ocf-shellfuncs: don't log but print to stderr if connected to a terminal
  + Medium: ocf-shellfuncs: don't output to stderr if using syslog
  + Medium: oracle/oralsnr: improve exit codes if the environment isn't valid
  + Medium: RA: iSCSILogicalUnit: fix monitor for STGT
  + Medium: RA: make sure that OCF_RESKEY_CRM_meta_interval is always defined (LF 2284)
  + Medium: RA: ManageRAID: require bash
  + Medium: RA: ManageRAID: require bash
  + Medium: RA: VirtualDomain: bail out early if config file can't be read during probe (Novell 593988)
  + Medium: RA: VirtualDomain: fix incorrect use of __OCF_ACTION
  + Medium: RA: VirtualDomain: improve error messages
  + Medium: RA: VirtualDomain: spin on define until we definitely have a domain name
  + Medium: Route: add route table parameter (lf#2335)
  + Medium: sfex: don't use pid file (lf#2363,bnc#585416)
  + Medium: sfex: exit with success on stop if sfex has never been started (bnc#585416)

* Tue Mar  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.9-1
- new upstream release
  Resolves: rhbz#569959
- spec file update:
  * update spec file copyright date
  * use bz2 tarball

* Thu Feb 25 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.7-5
- Resolves: rhbz#568010
- Do not build resource-agents on s390 and s390x.

* Mon Feb 22 2010 Marek Grac <mgrac@redhat.com> - 3.0.7-4
- Checksum error occurs on HA-LVM
- status on clusterfs "gfs" returned 1 (generic error)
- Resolves rhbz#563555 rhbz#558664

* Fri Feb 19 2010 Marek Grac <mgrac@redhat.com> - 3.0.7-3
- resource-agents can't be used by Pacemaker
- Resolves: rhbz#566176

* Wed Jan 13 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.7-2
- Drop support for drbd and smb (PM-drop-support-for-drbd-and-smb-resource-agents.patch)
- Explicitly list python as BuildRequires

* Mon Jan 11 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.7-1
- New rgmanager resource agents upstream release

* Mon Jan 11 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.6-2
- Update Pacameker agents to upstream version: c76b4a6eb576
  + High: RA: VirtualDomain: fix forceful stop (LF 2283)
  + High: apache: monitor operation of depth 10 for web applications (LF 2234)
  + Medium: IPaddr2: CLUSTERIP/iptables rule not always inserted on failed monitor (LF 2281)
  + Medium: RA: Route: improve validate (LF 2232)
  + Medium: mark obsolete RAs as deprecated (LF 2244)
  + Medium: mysql: escalate stop to KILL if regular shutdown doesn't work

* Mon Dec 7 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.6-1
- New rgmanager resource agents upstream release
- spec file update:
  * use global instead of define
  * use new Source0 url
  * use %name macro more aggressively

* Mon Dec 7 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.5-2
- Update Pacameker agents to upstream version: bc00c0b065d9
  + High: RA: introduce OCF_FUNCTIONS_DIR, allow it to be overridden (LF2239)
  + High: doc: add man pages for all RAs (LF2237)
  + High: syslog-ng: new RA
  + High: vmware: make meta-data work and several cleanups (LF 2212)
  + Medium: .ocf-shellfuncs: add ocf_is_probe function
  + Medium: Dev: make RAs executable (LF2239)
  + Medium: IPv6addr: ifdef out the ip offset hack for libnet v1.1.4 (LF 2034)
  + Medium: add mercurial repository version information to .ocf-shellfuncs
  + Medium: build: add perl-MailTools runtime dependency to ldirectord package (LF 1469)
  + Medium: iSCSITarget, iSCSILogicalUnit: support LIO
  + Medium: nfsserver: use check_binary properly in validate (LF 2211)
  + Medium: nfsserver: validate should not check if nfs_shared_infodir exists (thanks to eelco@procolix.com) (LF 2219)
  + Medium: oracle/oralsnr: export variables properly
  + Medium: pgsql: remove the previous backup_label if it exists
  + Medium: postfix: fix double stop (thanks to Dinh N. Quoc)
  + RA: LVM: Make monitor operation quiet in logs (bnc#546353)
  + RA: Xen: Remove instance_attribute "allow_migrate" (bnc#539968)
  + ldirectord: OCF agent: overhaul

* Fri Nov 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.5-1
- New rgmanager resource agents upstream release

* Wed Oct 28 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.4-2
- Update Pacameker agents to upstream version: e2338892f59f
  + High: send_arp - turn on unsolicited mode for compatibilty with the libnet version's exit codes
  + High: Trap sigterm for compatibility with the libnet version of send_arp
  + Medium: Bug - lf#2147: IPaddr2: behave if the interface is down
  + Medium: IPv6addr: recognize network masks properly
  + Medium: RA: VirtualDomain: avoid needlessly invoking "virsh define"

* Wed Oct 21 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.4-1
- New rgmanager resource agents upstream release

* Mon Oct 12 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.3-3
- Update Pacameker agents to upstream version: 099c0e5d80db
  + Add the ha_parameter function back into .ocf-shellfuncs.
  + Bug bnc#534803 - Provide a default for MAILCMD
  + Fix use of undefined macro @HA_NOARCHDATAHBDIR@
  + High (LF 2138): IPsrcaddr: replace 0/0 with proper ip prefix (thanks to Michael Ricordeau and Michael Schwartzkopff)
  + Import shellfuncs from heartbeat as badly written RAs use it
  + Medium (LF 2173): nfsserver: exit properly in nfsserver_validate
  + Medium: RA: Filesystem: implement monitor operation
  + Medium: RA: VirtualDomain: loop on status if libvirtd is unreachable
  + Medium: RA: VirtualDomain: loop on status if libvirtd is unreachable (addendum)
  + Medium: RA: iSCSILogicalUnit: use a 16-byte default SCSI ID
  + Medium: RA: iSCSITarget: be more persistent deleting targets on stop
  + Medium: RA: portblock: add per-IP filtering capability
  + Medium: mysql-proxy: log_level and keepalive parameters
  + Medium: oracle: drop spurious output from sqlplus
  + RA: Filesystem: allow configuring smbfs mounts as clones

* Wed Sep 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.3-1
- New rgmanager resource agents upstream release

* Thu Aug 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.1-1
- New rgmanager resource agents upstream release

* Tue Aug 18 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.0-16
- Create an ldirectord package
- Update Pacameker agents to upstream version: 2198dc90bec4
  + Build: Import ldirectord.
  + Ensure HA_VARRUNDIR has a value to substitute
  + High: Add findif tool (mandatory for IPaddr/IPaddr2)
  + High: IPv6addr: new nic and cidr_netmask parameters
  + High: postfix: new resource agent
  + Include license information
  + Low (LF 2159): Squid: make the regexp match more precisely output of netstat
  + Low: configure: Fix package name.
  + Low: ldirectord: add dependency on $remote_fs.
  + Low: ldirectord: add mandatory required header to init script.
  + Medium (LF 2165): IPaddr2: remove all colons from the mac address before passing it to send_arp
  + Medium: VirtualDomain: destroy domain shortly before timeout expiry
  + Medium: shellfuncs: Make the mktemp wrappers work.
  + Remove references to Echo function
  + Remove references to heartbeat shellfuncs.
  + Remove useless path lookups
  + findif: actually include the right header. Simplify configure.
  + ldirectord: Remove superfluous configure artifact.
  + ocf-tester: Fix package reference and path to DTD.

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 3.0.0-15
- Use bzipped upstream hg tarball.

* Wed Jul 29 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-14
- Merge Pacemaker cluster resource agents:
  * Add Source1.
  * Drop noarch. We have real binaries now.
  * Update BuildRequires.
  * Update all relevant prep/build/install/files/description sections.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  8 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-12
- spec file updates:
  * Update copyright header
  * final release.. undefine alphatag

* Thu Jul  2 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-11.rc4
- New upstream release.

* Sat Jun 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-10.rc3
- New upstream release.

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-9.rc2
- New upstream release + git94df30ca63e49afb1e8aeede65df8a3e5bcd0970

* Tue Mar 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-8.rc1
- New upstream release.
- Update BuildRoot usage to preferred versions/names

* Mon Mar  9 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-7.beta1
- New upstream release.

* Fri Mar  6 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-6.alpha7
- New upstream release.

* Tue Mar  3 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-5.alpha6
- New upstream release.

* Tue Feb 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-4.alpha5
- Drop Conflicts with rgmanager.

* Mon Feb 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-3.alpha5
- New upstream release.

* Thu Feb 19 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-2.alpha4
- Add comments on how to build this package.

* Thu Feb  5 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-1.alpha4
- New upstream release.
- Fix datadir/cluster directory ownership.

* Tue Jan 27 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-1.alpha3
  - Initial packaging
