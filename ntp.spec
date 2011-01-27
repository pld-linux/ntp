# TODO:
# - enable and package ntpdsim?
# - net-snmp-ntpd needs initscript
#
# Conditional build:
%bcond_without	avahi  # disable DNS-SD support via Avahi

%include	/usr/lib/rpm/macros.perl
Summary:	Network Time Protocol utilities
Summary(pl.UTF-8):	Narzędzia do synchronizacji czasu (Network Time Protocol)
Summary(pt_BR.UTF-8):	Network Time Protocol versão 4
Name:		ntp
Version:	4.2.6p1
Release:	4
License:	distributable
Group:		Networking/Daemons
Source0:	http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/%{name}-%{version}.tar.gz
# Source0-md5:	0510396dfbde40678b92f808ec07c0d2
Source1:	%{name}.conf
Source2:	%{name}.keys
Source3:	%{name}.init
Source4:	%{name}.sysconfig
Source5:	%{name}-client.init
Source6:	%{name}-client.sysconfig
Source7:	%{name}-manpages.tar.gz
# Source7-md5:	208fcc9019e19ab26d28e4597290bffb
Source8:	%{name}.upstart
Patch0:		%{name}-time.patch
Patch1:		%{name}-no_libelf.patch
Patch2:		%{name}-ipv6.patch
Patch3:		%{name}-openssl_check.patch
Patch4:		%{name}-nano.patch
Patch5:		%{name}-ntpdc-link_order.patch
Patch6:		%{name}-no_avahi.patch
# FC patches + 100
Patch101:	%{name}-4.2.6p1-sleep.patch
Patch102:	%{name}-4.2.6p1-droproot.patch
Patch103:	%{name}-4.2.6p1-bcast.patch
Patch104:	%{name}-4.2.6p1-cmsgalign.patch
Patch105:	%{name}-4.2.6p1-linkfastmath.patch
Patch106:	%{name}-4.2.6p1-tentative.patch
Patch107:	%{name}-4.2.6p1-retcode.patch
Patch108:	%{name}-4.2.6p1-rtnetlink.patch
Patch109:	%{name}-4.2.6p1-html2man.patch
Patch110:	%{name}-4.2.6p1-htmldoc.patch
Patch112:	%{name}-4.2.4p7-getprecision.patch
Patch113:	%{name}-4.2.6p1-logdefault.patch
Patch114:	%{name}-4.2.6p1-mlock.patch
URL:		http://www.ntp.org/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_avahi:BuildRequires:	avahi-compat-libdns_sd-devel}
BuildRequires:	libcap-devel
BuildRequires:	libnl-devel
BuildRequires:	libtool
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.561
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ntp
%define		_bindir		%{_sbindir}
%define		mibdir		%{_datadir}/mibs

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

%package -n ntpd
Summary:	The NTP daemon
Summary(pl.UTF-8):	Narzędzia do synchronizacji czasu (Network Time Protocol)
Summary(pt_BR.UTF-8):	Network Time Protocol versão 4
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts >= 0.4.3.0
Provides:	group(ntp)
Provides:	ntp = %{version}-%{release}
Provides:	ntpdaemon
Provides:	user(ntp)
Obsoletes:	ntp < 4.2.4p8-6
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

%package -n ntpd-upstart
Summary:	Upstart job description for the NTP daemon
Summary(pl.UTF-8):	Opis zadania Upstart dla demona NTP
Group:		Daemons
Requires:	ntpd = %{version}-%{release}
Requires:	upstart >= 0.6

%description -n ntpd-upstart
Upstart job description for the NTP daemon.

%description -n ntpd-upstart -l pl.UTF-8
Opis zadania Upstart dla demona NTP.

%package -n ntpdate
Summary:	Utility to set the date and time via NTP
Summary(pl.UTF-8):	Klient do synchronizacji czasu po NTP (Network Time Protocol)
Group:		Applications/Networking
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts >= 0.4.3.0
Provides:	group(ntp)
Provides:	user(ntp)
Conflicts:	ntp < 4.2.0-3
# for upgrades
Provides:	ntp-client = %{version}-%{release}
Obsoletes:	ntp-client < 4.2.4p8-6
# virtual
Provides:	ntpclient
Obsoletes:	ntpclient

%description -n ntpdate
ntpdate is a program for retrieving the date and time from NTP
servers.

%description -n ntpdate -l pl.UTF-8
Klient do synchronizacji czasu po NTP (Network Time Protocol).

%package -n mibs-ntp
Summary:	MIBs for NTP time entities
Group:		Applications/System
Requires:	mibs-dirs

%description -n mibs-ntp
The Management Information Base for NTP time entities.

%package -n net-snmp-ntpd
Summary:	NTP SNMP subagent for Net-SNMP
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	net-snmp
Requires:	rc-scripts
Suggests:	mibs-ntp

%description -n net-snmp-ntpd
NTP SNMP AgentX subagent for Net-SNMP.

%package tools
Summary:	NTP tools
Group:		Applications/Networking
Obsoletes:	ntp-ntptrace

%description tools
This package contains ntp tools:
- ntptrace: Trace a chain of NTP servers back to the primary source
- ntp-wait: Wait for NTP server to synchronize

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

%prep
%setup -q -a7
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%{!?with_avahi:%patch6 -p1}

## FC patches
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1

echo 'AM_CONDITIONAL([NEED_LIBOPTS], false)' >> configure.ac
echo 'AM_CONDITIONAL([NEED_LIBOPTS], false)' >> sntp/configure.ac

%build
%{__libtoolize}
%{__aclocal} -I m4 -I libopts/m4
%{__autoconf}
%{__automake}
cd sntp
%{__libtoolize}
%{__aclocal} -I ../m4 -I libopts/m4
%{__autoconf}
%{__automake}
cd ..

CPPFLAGS="%{rpmcppflags} -I/usr/include/readline"
%configure \
	--with-binsubdir=sbin \
	--enable-linuxcaps \
	--enable-getifaddrs \
	--enable-ipv6 \
	--with-lineeditlibs=readline \
	--with-crypto=openssl

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{rc.d/init.d,sysconfig,cron.hourly,init},%{_mandir}/man1}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/ntp.conf
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/keys
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/ntpd
install -p %{SOURCE5} $RPM_BUILD_ROOT/etc/rc.d/init.d/ntpdate
cp -a %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/ntpd
cp -a %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/ntpdate
install -p %{SOURCE8} $RPM_BUILD_ROOT/etc/init/ntpd.conf
cp -a man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

install -d $RPM_BUILD_ROOT/var/lib/ntp
touch $RPM_BUILD_ROOT/var/lib/ntp/drift

cat > $RPM_BUILD_ROOT/etc/cron.hourly/ntpdate <<'EOF'
#!/bin/sh
exec /sbin/service ntpdate cronsettime
EOF

install -d $RPM_BUILD_ROOT%{mibdir}
cp -a ntpsnmpd/ntpv4-mib.mib $RPM_BUILD_ROOT%{mibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n ntpd
%groupadd -g 246 ntp
%useradd -u 246 -d %{_sysconfdir} -g ntp -c "NTP Daemon" ntp

%post -n ntpd
/sbin/chkconfig --add ntpd
%service ntpd restart "NTP Daemon"

%preun -n ntpd
if [ "$1" = "0" ]; then
	%service ntpd stop
	/sbin/chkconfig --del ntpd
	rm -f /var/lib/ntp/drift
fi

%post -n ntpd-upstart
%upstart_post ntpd

%postun -n ntpd-upstart
%upstart_postun ntpd

%postun -n ntp
if [ "$1" = "0" ]; then
	%userremove ntp
	%groupremove ntp
fi


%pre -n ntpdate
%groupadd -g 246 ntp
%useradd -u 246 -d %{_sysconfdir} -g ntp -c "NTP Daemon" ntp

%post -n ntpdate
/sbin/chkconfig --add ntpdate
%service ntpdate restart "NTP Date"

%preun -n ntpdate
if [ "$1" = "0" ]; then
	%service ntpdate stop
	/sbin/chkconfig --del ntpdate
fi

%postun -n ntpdate
if [ "$1" = "0" ]; then
	%userremove ntp
	%groupremove ntp
fi

%triggerun -n ntpd -- ntp < 4.2.4p8-3.14
# Prevent preun from ntp from working
chmod a-x /etc/rc.d/init.d/ntpd

%triggerpostun -n ntpd -- ntp < 4.2.4p8-3.14
# Restore what triggerun removed
chmod 754 /etc/rc.d/init.d/ntpd
sed -i -e 's,/etc/ntp/drift,/var/lib/ntp/drift,' %{_sysconfdir}/ntp.conf
mv -f /etc/ntp/ntp.drift /var/lib/ntp/drift 2>/dev/null
mv -f /etc/ntp/drift /var/lib/ntp/drift 2>/dev/null
%service -q ntpd restart

%triggerpostun -n ntpdate -- ntp-client < 4.2.4p8-3.2
if [ -f /etc/sysconfig/ntp.rpmsave ]; then
	cp -f /etc/sysconfig/ntpdate{,.rpmnew}
	mv -f /etc/sysconfig/ntp.rpmsave /etc/sysconfig/ntpdate
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
%{_mandir}/man1/ntp-keygen.1*
%{_mandir}/man1/ntpq.1*
%{_mandir}/man1/ntptime.1*
%{_mandir}/man1/sntp.1*

%dir %attr(770,root,ntp) /var/lib/ntp
%attr(640,ntp,ntp) %ghost /var/lib/ntp/drift

%files -n ntpd-upstart
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/init/ntpd.conf

%files -n ntpdate
%defattr(644,root,root,755)
%doc COPYRIGHT
%attr(755,root,root) %{_sbindir}/ntpdate
%attr(754,root,root) /etc/rc.d/init.d/ntpdate
%attr(754,root,root) /etc/cron.hourly/ntpdate
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ntpdate
%{_mandir}/man1/ntpdate*

%files -n mibs-ntp
%defattr(644,root,root,755)
%{mibdir}/ntpv4-mib.mib

%files -n net-snmp-ntpd
%defattr(644,root,root,755)
%doc ntpsnmpd/README
%attr(755,root,root) %{_sbindir}/ntpsnmpd
%{_mandir}/man1/ntpsnmpd.1*

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ntptrace
%attr(755,root,root) %{_sbindir}/ntp-wait
%{_mandir}/man1/ntptrace*

%files doc-html
%defattr(644,root,root,755)
%doc html/*
