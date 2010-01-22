# TODO
# - run as ntp/ntp (fc patches)
# - default config is too restrictive (ntpq -p should work locally)
%include	/usr/lib/rpm/macros.perl
Summary:	Network Time Protocol utilities
Summary(pl.UTF-8):	Narzędzia do synchronizacji czasu (Network Time Protocol)
Summary(pt_BR.UTF-8):	Network Time Protocol versão 4
Name:		ntp
Version:	4.2.4p8
Release:	3.1
License:	distributable
Group:		Daemons
Source0:	http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/%{name}-%{version}.tar.gz
# Source0-md5:	fe137056e7e611798a46971a783567ce
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
Patch6:		%{name}-nano.patch
Patch7:		%{name}-manpage.patch
URL:		http://www.ntp.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libcap-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ntp
%define		_bindir		%{_sbindir}

%description
The Network Time Protocol (NTP) is used to synchronize a computer's
time with another reference time source. The ntp package contains
utilities and daemons which will synchronize your computer's time to
Coordinated Universal Time (UTC) via the NTP protocol and NTP servers.

%description -l pl.UTF-8
Network Time Protocol (NTP) służy do synchronizacji czasu komputera z
innym, wzorcowym źródłem czasu. Pakiet ntp zawiera narzędzia i demony
służące do dokładnego synchronizowania czasu komputera według czasu
uniwersalnego (UTC) poprzez protokół NTP z serwerami NTP.

%description -l pt_BR.UTF-8
Esta é a versão 4 do Network Time Protocol (NTP). Este protocolo é
utilizado para sincronizar o relógio do computador com uma outra
referência de horário. Este pacote contém utilitários e servidores que
sincronizarão o relógio do seu computador com o horário universal
(UTC) através do protocolo NTP e utilizando servidores NTP públicos.

Instale o pacote ntp se você necessitar de ferramentas para manter o
relógio do seu computador constantemente atualizado.

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

%package -n ntpd
Summary:	The NTP daemon
Summary(pl.UTF-8):	Narzędzia do synchronizacji czasu (Network Time Protocol)
Summary(pt_BR.UTF-8):	Network Time Protocol versão 4
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.4.0.10
Provides:	ntp = %{version}-%{release}
Provides:	ntpdaemon
Obsoletes:	ntp < 4.2.4p8-4
Obsoletes:	ntpdaemon
Obsoletes:	openntpd
Obsoletes:	xntp3

%description -n ntpd
The Network Time Protocol (NTP) is used to synchronize a computer's
time with another reference time source. The ntp package contains
utilities and daemons which will synchronize your computer's time to
Coordinated Universal Time (UTC) via the NTP protocol and NTP servers.

This package includes ntpd (a daemon which continuously adjusts system
time)

%description -n ntpd -l pl.UTF-8
Network Time Protocol (NTP) służy do synchronizacji czasu komputera z
innym, wzorcowym źródłem czasu. Pakiet ntp zawiera narzędzia i demony
służące do dokładnego synchronizowania czasu komputera według czasu
uniwersalnego (UTC) poprzez protokół NTP z serwerami NTP.

Pakiet ntp zawiera ntpd (demona, który w sposób ciągły aktualizuje
czas systemowy)

%description -n ntpd -l pt_BR.UTF-8
Esta é a versão 4 do Network Time Protocol (NTP). Este protocolo é
utilizado para sincronizar o relógio do computador com uma outra
referência de horário. Este pacote contém utilitários e servidores que
sincronizarão o relógio do seu computador com o horário universal
(UTC) através do protocolo NTP e utilizando servidores NTP públicos.

%package -n ntpdate
Summary:	Utility to set the date and time via NTP
Summary(pl.UTF-8):	Klient do synchronizacji czasu po NTP (Network Time Protocol)
Group:		Applications/Networking
Requires(post,preun):	/sbin/chkconfig
Provides:	ntpclient
Obsoletes:	ntpclient
Conflicts:	ntp < 4.2.0-3
# for upgrades
Provides:	ntp-client = %{version}-%{release}
Obsoletes:	ntp-client < 4.2.4p8-4

%description -n ntpdate
ntpdate is a program for retrieving the date and time from NTP
servers.

%description -n ntpdate -l pl.UTF-8
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
%patch6 -p1
%patch7	-p0

echo 'AM_CONDITIONAL([NEED_LIBOPTS], false)' >> configure.ac
echo 'AM_CONDITIONAL([NEED_LIBOPTS], false)' >> sntp/configure.ac

%build
%{__libtoolize}
%{__aclocal} -I m4 -I libopts/m4
%{__autoconf}
%{__automake}
cd sntp
%{__libtoolize}
%{__aclocal} -I libopts/m4
%{__autoconf}
%{__automake}
cd ..

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

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/ntp.conf
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/keys
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/ntpd
install -p %{SOURCE5} $RPM_BUILD_ROOT/etc/rc.d/init.d/ntpdate
cp -a %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/ntpd
cp -a %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/ntpdate
cp -a man/*.1  $RPM_BUILD_ROOT%{_mandir}/man1

cat > $RPM_BUILD_ROOT/etc/cron.hourly/ntpdate <<'EOF'
#!/bin/sh
/sbin/service ntpdate cronsettime
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post -n ntpd
/sbin/chkconfig --add ntpd
%service ntpd restart "NTP Daemon"

%preun -n ntpd
if [ "$1" = "0" ]; then
	%service ntpd stop
	/sbin/chkconfig --del ntpd
	rm -f /etc/ntp/drift
fi

%post -n ntpdate
/sbin/chkconfig --add ntpdate
%service ntpdate restart "NTP Date"

%preun -n ntpdate
if [ "$1" = "0" ]; then
	%service ntpdate stop
	/sbin/chkconfig --del ntpdate
fi

%files -n ntpd
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

%files -n ntpdate
%defattr(644,root,root,755)
%doc COPYRIGHT
%attr(755,root,root) %{_sbindir}/ntpdate
%attr(754,root,root) /etc/rc.d/init.d/ntpdate
%attr(754,root,root) /etc/cron.hourly/ntpdate
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ntpdate
%{_mandir}/man1/ntpdate*

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ntptrace
%attr(755,root,root) %{_sbindir}/ntp-wait
%{_mandir}/man1/ntptrace*

%files doc-html
%defattr(644,root,root,755)
%doc html/*
