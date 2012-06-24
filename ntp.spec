%include	/usr/lib/rpm/macros.perl
Summary:	Network Time Protocol utilities
Summary(pl):	Narz�dzia do synchronizacji czasu (Network Time Protocol)
Summary(pt_BR):	Network Time Protocol vers�o 4
Name:		ntp
Version:	4.2.0
Release:	19.1
License:	distributable
Group:		Daemons
Source0:	ftp://ftp.udel.edu/pub/ntp/ntp4/%{name}-%{version}.tar.gz
# Source0-md5:	0f8fabe87cf54f409b57c6283f0c0c3d
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
Patch4:		%{name}-gcc4.patch
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

%description -l pl
Network Time Protocol (NTP) s�u�y do synchronizacji czasu komputera z
innym, wzorcowym �r�d�em czasu. Pakiet ntp zawiera narz�dzia i demony
s�u��ce do dok�adnego synchronizowania czasu komputera wed�ug czasu
uniwersalnego (UTC) poprzez protok� NTP z serwerami NTP. Pakiet ntp
zawiera ntpd (demona, kt�ry w spos�b ci�g�y aktualizuje czas
systemowy), natomiast pakiet ntp-client zawiera program ntpdate
(program do odczytywania daty i czasu z innych maszyn po sieci).

%description -l pt_BR
Esta � a vers�o 4 do Network Time Protocol (NTP). Este protocolo �
utilizado para sincronizar o rel�gio do computador com uma outra
refer�ncia de hor�rio. Este pacote cont�m utilit�rios e servidores que
sincronizar�o o rel�gio do seu computador com o hor�rio universal
(UTC) atrav�s do protocolo NTP e utilizando servidores NTP p�blicos.

Instale o pacote ntp se voc� necessitar de ferramentas para manter o
rel�gio do seu computador constantemente atualizado.

Este pacote obsoleta o antigo xntp3.

%package ntptrace
Summary:	Trace a chain of NTP servers back to the primary source
Summary(pl):	�ledzenie �a�cucha serwer�w NTP a� do g��wnego �r�d�a
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}

%description ntptrace
ntptrace determines where a given Network Time Protocol (NTP) server
gets its time from, and follows the chain of NTP servers back to their
master time source.

%description ntptrace -l pl
ntptrace okre�la sk�d dany serwer NTP (Network Time Protocol) pobiera
sw�j czas i pod��a �a�cuchem serwer�w NTP a� do g��wnego �r�d�a czasu.

%package doc-html
Summary:	HTML documentation for ntp
Summary(pl):	Dokumentacja HTML dla ntp
Summary(pt_BR):	Documenta��o adicional para o pacote ntp
Group:		Documentation

%description doc-html
HTML documentation for ntp.

%description doc-html -l pl
Dokumentacja do ntp w HTML.

%description doc-html -l pt_BR
Este pacote cont�m documenta��o adicional sobre o NTP vers�o 4.

%package client
Summary:	Network Time Protocol client
Summary(pl):	Klient do synchronizacji czasu po NTP (Network Time Protocol)
Group:		Applications/Networking
Conflicts:	ntp < 4.2.0-3

%description client
Network Time Protocol client.

%description doc-html -l pl
Klient do synchronizacji czasu po NTP (Network Time Protocol).

%prep
%setup -q -a7
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
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
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/ntpd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ntpd
%{_mandir}/man1/*
%exclude %{_mandir}/man1/ntpdate*
%exclude %{_mandir}/man1/ntptrace*
%exclude %{_sbindir}/ntpdate
%exclude %{_sbindir}/ntptrace

%files ntptrace
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ntptrace
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
