#
# spec file for package iptables
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           iptables
%define lname_ipq	libipq
%define lname_iptc	libiptc
%define lname_xt	libxtables
Version:        1.4.14
Release:        0
License:        GPL-2.0+
Summary:        IP Packet Filter Administration utilities
Group:          Productivity/Networking/Security

Url:            http://netfilter.org/
#DL-URL:	ftp://ftp.netfilter.org/pub/iptables/
#Git-Web:	http://git.netfilter.org/
#Git-Clone:	git://git.netfilter.org/iptables
Source:         ftp://ftp.netfilter.org/pub/iptables/%{name}-%{version}.tar.bz2
Source2:        ftp://ftp.netfilter.org/pub/iptables/%{name}-%{version}.tar.bz2.sig
Patch1:         iptables-batch.patch
Patch2:         iptables-apply-mktemp-fix.patch
BuildRequires:  fdupes
BuildRequires:  libtool
BuildRequires:  pkgconfig >= 0.21
BuildRequires:  pkgconfig(libnfnetlink) >= 1.0.0
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
iptables is used to set up, maintain, and inspect the tables of IP
packet filter rules in the Linux kernel. This version requires kernel
2.4.0 or newer.

%package -n %lname_ipq
Summary:        Library to interface with the (old) ip_queue kernel mechanism
Group:          System/Libraries

%description -n %lname_ipq
The Netfilter project provides a mechanism (ip_queue) for passing
packets out of the stack for queueing to userspace, then receiving
these packets back into the kernel with a verdict specifying what to
do with the packets (such as ACCEPT or DROP). These packets may also
be modified in userspace prior to reinjection back into the kernel.

ip_queue/libipq is obsoleted by nf_queue/libnetfilter_queue!

%package -n libipq-devel
Summary:        Development files for the ip_queue kernel mechanism
Group:          Development/Libraries/C and C++
Requires:       %lname_ipq = %{version}

%description -n libipq-devel
The Netfilter project provides a mechanism (ip_queue) for passing
packets out of the stack for queueing to userspace, then receiving
these packets back into the kernel with a verdict specifying what to
do with the packets (such as ACCEPT or DROP). These packets may also
be modified in userspace prior to reinjection back into the kernel.

ip_queue/libipq is obsoleted by nf_queue/libnetfilter_queue!

%package -n %lname_iptc
Summary:        Library for low-level ruleset generation and parsing
Group:          System/Libraries

%description -n %lname_iptc
libiptc ("iptables cache") is used to retrieve from the kernel, parse,
construct, and load new rulesets into the kernel.

%package -n libiptc-devel
Summary:        Development files for libiptc, a packet filter ruleset library
Group:          Development/Libraries/C and C++
Requires:       %lname_iptc = %{version}
# NOT adding Obsoletes/Provides: iptables-devel, because that one has
# been split into _two_ new pkgs (libxtables-devel, libiptc-devel).
# NOTE: Please use pkgconfig(...) symbols for BuildRequires.

%description -n libiptc-devel
libiptc ("iptables cache") is used to retrieve from the kernel, parse,
construct, and load new rulesets into the kernel.

%package -n %lname_xt
Summary:        iptables extension interface
Group:          System/Libraries

%description -n %lname_xt
This library contains all the iptables code shared between iptables,
ip6tables, their extensions, and for external integration for e.g.
iproute2's m_xt.

%package -n libxtables-devel
Summary:        Libraries, Headers and Development Man Pages for iptables
Group:          Development/Libraries/C and C++
Requires:       %lname_xt = %{version}

%description -n libxtables-devel
This library contains all the iptables code shared between iptables,
ip6tables, their extensions, and for external integration for e.g.

Link your extension (iptables plugins) with $(pkg-config xtables
--libs) and place the plugin in the directory given by $(pkg-config
xtables --variable=xtlibdir).

%prep
%if 0%{?__xz:1}
%setup -q
%else
tar -xf "%{SOURCE0}" --use=bzip2;
%setup -DTq
%endif
%patch1 -p1
%patch2 -p1

%build
if [ ! -e configure ]; then
	./autogen.sh;
fi
# bnc#561793 - do not include unclean module in iptables manpage
rm -f extensions/libipt_unclean.man
# includedir is overriden on purpose to detect projects that
# fail to include libxtables_CFLAGS
%configure --includedir=%{_includedir}/%{name}-%{version} --enable-libipq
make %{?_smp_mflags}

%install
%make_install
# iptables-apply is not installed by upstream Makefile
install -m0755 iptables/iptables-apply %{buildroot}%{_sbindir}/
install -m0644 iptables/iptables-apply.8 %{buildroot}%{_mandir}/man8/
rm -f "%{buildroot}/%{_libdir}"/*.la;
%fdupes %{buildroot}

%post -n %lname_ipq -p /sbin/ldconfig

%postun -n %lname_ipq -p /sbin/ldconfig

%post -n %lname_iptc -p /sbin/ldconfig

%postun -n %lname_iptc -p /sbin/ldconfig

%post -n %lname_xt -p /sbin/ldconfig

%postun -n %lname_xt -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING
%doc %{_mandir}/man1/*
%doc %{_mandir}/man8/*
%{_bindir}/iptables*
%{_sbindir}/iptables*
%{_sbindir}/ip6tables*
%{_sbindir}/xtables*
%{_sbindir}/nfnl_osf
%{_libdir}/xtables
%{_datadir}/xtables

%files -n %lname_ipq
%defattr(-,root,root)
%{_libdir}/libipq.so.0*

%files -n libipq-devel
%defattr(-,root,root)
%doc %{_mandir}/man3/libipq*
%doc %{_mandir}/man3/ipq*
%dir %{_includedir}/%{name}-%{version}
%{_includedir}/%{name}-%{version}/libipq*
%{_libdir}/libipq.so
%{_libdir}/pkgconfig/libipq.pc

%files -n %lname_iptc
%defattr(-,root,root)
%{_libdir}/libiptc.so.0*
%{_libdir}/libip4tc.so.0*
%{_libdir}/libip6tc.so.0*

%files -n libiptc-devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}-%{version}
%{_includedir}/%{name}-%{version}/libiptc*
%{_libdir}/libip*tc.so
%{_libdir}/pkgconfig/libip*tc.pc

%files -n %lname_xt
%defattr(-,root,root)
%{_libdir}/libxtables.so.7*

%files -n libxtables-devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}-%{version}
%{_includedir}/%{name}-%{version}/xtables.h
%{_libdir}/libxtables.so
%{_libdir}/pkgconfig/xtables.pc

%changelog
