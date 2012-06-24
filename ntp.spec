Summary:	Network Time Protocol utilities
Summary(pl):	Narz�dzia do synchronizacji czasu (Network Time Protocol)
Summary(pt_BR):	Network Time Protocol vers�o 4
Name:		ntp
Version:	4.2.0
Release:	3
License:	distributable
Group:		Daemons
Source0:	ftp://ftp.udel.edu/pub/ntp/ntp4/%{name}-%{version}.tar.gz
# Source0-md5:	0f8fabe87cf54f409b57c6283f0c0c3d
Source1:	%{name}.conf
Source2:	%{name}.keys
Source3:	%{name}.init
Source4:	%{name}.sysconfig
Source5:	%{name}d.8
Source6:	%{name}date.8
Source7:	%{name}-client.init
Source8:	%{name}-client.sysconfig
Patch0:		%{name}-time.patch
Patch1:		%{name}-no_libelf.patch
URL:		http://www.ntp.org/
BuildRequires:	automake
BuildRequires:	readline-devel >= 4.2
Requires(post,preun):	/sbin/chkconfig
PreReq:		rc-scripts
Obsoletes:	xntp3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ntp
%define		_bindir		%{_sbindir}

%description
The Network Time Protocol (NTP) is used to synchronize a computer's
time with another reference time source. The ntp package contains
utilities and daemons which will synchronize your computer's time to
Coordinated Universal Time (UTC) via the NTP protocol and NTP servers.
The ntp package includes ntpdate (a program for retrieving the date
and time from remote machines via a network) and ntpd (a daemon which
continuously adjusts system time).

%description -l pl
Pakiet zawiera narz�dzia i demony s�u��ce do dok�adnego
synchronizowania czasu Twojego komputera: ntpdate, program podobny do
rdate oraz ntpd, demon aktualizuj�cy czas w spos�b ci�g�y.

%description -l pt_BR
Esta � a vers�o 4 do Network Time Protocol (NTP). Este protocolo �
utilizado para sincronizar o rel�gio do computador com uma outra
refer�ncia de hor�rio. Este pacote cont�m utilit�rios e servidores
que sincronizar�o o rel�gio do seu computador com o hor�rio universal
(UTC) atrav�s do protocolo NTP e utilizando servidores NTP p�blicos.

Instale o pacote ntp se voc� necessitar de ferramentas para manter o
rel�gio do seu computador constantemente atualizado.

Este pacote obsoleta o antigo xntp3.

%package doc-html
Summary:	HTML documentation for ntp
Summary(pl):	Dokumentacja HTML dla ntp
Summary(pt_BR):	Documenta��o adicional para o pacote ntp
Group:		Daemons

%description doc-html
HTML documentation for ntp.

%description doc-html -l pl
Dokumentacja do ntp w HTML.

%description doc-html -l pt_BR
Este pacote cont�m documenta��o adicional sobre o NTP vers�o 4.

%package client
Summary:	Network Time Protocol client
Summary(pl):	Klient do synchronizacji czasu (Network Time Protocol)
Group:		Applications

%description client
Network Time Protocol client

%description doc-html -l pl
Klient do synchronizacji czasu (Network Time Protocol)

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp /usr/share/automake/config.sub .
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{rc.d/init.d,sysconfig},%{_mandir}/man8}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/ntp.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/keys
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/ntpd
install %{SOURCE7} $RPM_BUILD_ROOT/etc/rc.d/init.d/ntp
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/ntpd
install %{SOURCE8} $RPM_BUILD_ROOT/etc/sysconfig/ntp
install %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE6} $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ntpd
if [ -f /var/lock/subsys/ntpd ]; then
	/etc/rc.d/init.d/ntpd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/ntpd start\" to start ntpd daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ntpd ]; then
		/etc/rc.d/init.d/ntpd stop >&2
	fi
	/sbin/chkconfig --del ntpd
fi

%post client
/sbin/chkconfig --add ntp
if [ -f /var/lock/subsys/ntp ]; then
	/etc/rc.d/init.d/ntp restart >&2
else
	echo "Run \"/etc/rc.d/init.d/ntp start\" to start ntp."
fi

%preun client
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ntp ]; then
		/etc/rc.d/init.d/ntp stop >&2
	fi
	/sbin/chkconfig --del ntp
fi

%files
%defattr(644,root,root,755)
%doc NEWS TODO WHERE-TO-START conf/*.conf
%attr(750,root,root) %dir %{_sysconfdir}/*
%attr(640,root,root) %config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/ntpd
%attr(640,root,root) %config %verify(not size md5 mtime) /etc/sysconfig/ntpd
%{_mandir}/man8/*
%exclude %{_mandir}/man8/ntpdate*
%exclude %{_sbindir}/ntpdate

%files doc-html
%defattr(644,root,root,755)
%doc html/*

%files client
%attr(755,root,root) %{_sbindir}/ntpdate
%attr(754,root,root) /etc/rc.d/init.d/ntp
%attr(640,root,root) %config %verify(not size md5 mtime) /etc/sysconfig/ntp
%{_mandir}/man8/ntpdate*
