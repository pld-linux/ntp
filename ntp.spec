# TODO
# - update manual pages (from debian?)
%include	/usr/lib/rpm/macros.perl
Summary:	Network Time Protocol utilities
Summary(pl.UTF-8):	Narzędzia do synchronizacji czasu (Network Time Protocol)
Summary(pt_BR.UTF-8):	Network Time Protocol versão 4
Name:		ntp
Version:	4.2.4p4
Release:	4
License:	distributable
Group:		Daemons
Source0:	http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/%{name}-%{version}.tar.gz
# Source0-md5:	fcb32a01e1ae3f9ed5bac86b12c7a1cc
Source1:	%{name}.conf
Source2:	%{name}.keys
Source3:	%{name}.init
Source4:	%{name}.sysconfig
Source5:	%{name}-client.init
Source6:	%{name}-client.sysconfig
Source7:	%{name}-manpages.tar.gz
# Source7-md5:	208fcc9019e19ab26d28e4597290bffb
Patch0:		%{name}-time.patch
Patch1:		%{name}-no_libelf.patch
Patch2:		%{name}-ipv6.patch
Patch3:		%{name}-openssl_check.patch
Patch4:		%{name}-clock_settime.patch
Patch5:		%{name}-md5.patch
URL:		http://www.ntp.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.4.0.10
Obsoletes:	xntp3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ntp
%define		_bindir		%{_sbindir}

%description
The Network Time Protocol (NTP) is used to synchronize a computer's
time with another reference time source. The ntp package contains
utilities and daemons which will synchronize your computer's time to
Coordinated Universal Time (UTC) via the NTP protocol and NTP servers.
ntp package includes ntpd (a daemon which continuously adjusts system
time), while ntp-client package contains ntpdate (a program for
retrieving the date and time from remote machines via a network).

%description -l pl.UTF-8
Network Time Protocol (NTP) służy do synchronizacji czasu komputera z
innym, wzorcowym źródłem czasu. Pakiet ntp zawiera narzędzia i demony
służące do dokładnego synchronizowania czasu komputera według czasu
uniwersalnego (UTC) poprzez protokół NTP z serwerami NTP. Pakiet ntp
zawiera ntpd (demona, który w sposób ciągły aktualizuje czas
systemowy), natomiast pakiet ntp-client zawiera program ntpdate
(program do odczytywania daty i czasu z innych maszyn po sieci).

%description -l pt_BR.UTF-8
Esta é a versão 4 do Network Time Protocol (NTP). Este protocolo é
utilizado para sincronizar o relógio do computador com uma outra
referência de horário. Este pacote contém utilitários e servidores que
sincronizarão o relógio do seu computador com o horário universal
(UTC) através do protocolo NTP e utilizando servidores NTP públicos.

Instale o pacote ntp se você necessitar de ferramentas para manter o
relógio do seu computador constantemente atualizado.

Este pacote obsoleta o antigo xntp3.

%package doc-html
Summary:	HTML documentation for ntp
Summary(pl.UTF-8):	Dokumentacja HTML dla ntp
Summary(pt_BR.UTF-8):	Documentação adicional para o pacote ntp
Group:		Documentation

%description doc-html
HTML documentation for ntp.

%description doc-html -l pl.UTF-8
Dokumentacja do ntp w HTML.

%description doc-html -l pt_BR.UTF-8
Este pacote contém documentação adicional sobre o NTP versão 4.

%package client
Summary:	Network Time Protocol client
Summary(pl.UTF-8):	Klient do synchronizacji czasu po NTP (Network Time Protocol)
Group:		Applications/Networking
Requires(post,preun):	/sbin/chkconfig
Conflicts:	ntp < 4.2.0-3

%description client
Network Time Protocol client.

%description client -l pl.UTF-8
Klient do synchronizacji czasu po NTP (Network Time Protocol).

%package tools
Summary:	NTP tools
Group:		Applications/Networking
Obsoletes:	ntp-ntptrace

%description tools
This package contains ntp tools:
- ntptrace: Trace a chain of NTP servers back to the primary source
- ntp-wait: Wait for NTP server to synchronize

%prep
%setup -q -a7
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p1

echo 'AM_CONDITIONAL([NEED_LIBOPTS], false)' >> configure.ac

%build
%{__libtoolize}
%{__aclocal} -I m4 -I libopts/m4
%{__autoconf}
%{__automake}
%configure \
	--with-binsubdir=sbin \
	--enable-linuxcaps \
	--enable-getifaddrs \
	--enable-ipv6 \
	--with-crypto=openssl

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{rc.d/init.d,sysconfig,cron.hourly},%{_mandir}/man1}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/ntp.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/keys
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/ntpd
install %{SOURCE5} $RPM_BUILD_ROOT/etc/rc.d/init.d/ntp
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/ntpd
install %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/ntp
install man/*.1  $RPM_BUILD_ROOT%{_mandir}/man1

cat > $RPM_BUILD_ROOT/etc/cron.hourly/ntp <<'EOF'
#!/bin/sh
/sbin/service ntp cronsettime
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ntpd
%service ntpd restart "ntpd daemon"

%preun
if [ "$1" = "0" ]; then
	%service ntpd stop
	/sbin/chkconfig --del ntpd
	rm -f /etc/ntp/drift
fi

%post client
/sbin/chkconfig --add ntp
%service ntp restart

%preun client
if [ "$1" = "0" ]; then
	%service ntp stop
	/sbin/chkconfig --del ntp
fi

%files
%defattr(644,root,root,755)
%doc NEWS TODO WHERE-TO-START conf/*.conf COPYRIGHT
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ntpd
%attr(754,root,root) /etc/rc.d/init.d/ntpd
%attr(755,root,root) %{_sbindir}/ntpd
%attr(755,root,root) %{_sbindir}/ntpdc
%attr(755,root,root) %{_sbindir}/ntp-keygen
%attr(755,root,root) %{_sbindir}/ntpq
%attr(755,root,root) %{_sbindir}/ntptime
%attr(755,root,root) %{_sbindir}/sntp
%attr(755,root,root) %{_sbindir}/tickadj
%{_mandir}/man1/ntpd.1*
%{_mandir}/man1/ntpdc.1*
%{_mandir}/man1/ntpdsim.1*
%{_mandir}/man1/ntp-keygen.1*
%{_mandir}/man1/ntpq.1*
%{_mandir}/man1/ntptime.1*
%{_mandir}/man1/sntp.1*

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ntptrace
%attr(755,root,root) %{_sbindir}/ntp-wait
%{_mandir}/man1/ntptrace*

%files doc-html
%defattr(644,root,root,755)
%doc html/*

%files client
%defattr(644,root,root,755)
%doc COPYRIGHT
%attr(755,root,root) %{_sbindir}/ntpdate
%attr(754,root,root) /etc/rc.d/init.d/ntp
%attr(754,root,root) /etc/cron.hourly/ntp
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ntp
%{_mandir}/man1/ntpdate*
