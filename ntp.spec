Summary:	Network Time Protocol utilities
Summary(pl):	Narzêdzia do synchronizacji czasu (Network Time Protocol)
Name:		ntp
Version:	4.1.0
Release:	5
License:	distributable
Group:		Daemons
Source0:	ftp://ftp.udel.edu/pub/ntp/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source2:	%{name}.keys
Source3:	%{name}.init
Source4:	%{name}.sysconfig
Source5:	ntpd.8
Source6:	ntpdate.8
Patch0:		%{name}-time.patch
Patch1:		%{name}-vsnprintf.patch
URL:		http://www.ntp.org/
BuildConflicts:	libelf
BuildRequires:	readline-devel >= 4.2
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
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
Pakiet zawiera narzêdzia i demony s³u¿±ce do dok³adnego
synchronizowania czasu Twojego komputera: ntpdate, program podobny do
rdate oraz ntpd, demon aktualizuj±cy czas w sposób ci±g³y.

%package doc-html
Summary:	HTML documentation for ntp
Summary(pl):	Dokumentacja HTML dla ntp
Group:		Daemons

%description doc-html
HTML documentation for ntp.

%description doc-html -l pl
Dokumentacja do ntp w HTML.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{rc.d/init.d,sysconfig},%{_mandir}/man8}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/ntp.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/keys
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/ntp
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/ntp
install %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE6} $RPM_BUILD_ROOT%{_mandir}/man8

gzip -9nf NEWS TODO conf/*.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ntp
if [ -f /var/lock/subsys/ntp ]; then
	/etc/rc.d/init.d/ntp restart >&2
else
	echo "Run \"/etc/rc.d/init.d/ntp start\" to start ntp daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ntp ]; then
		/etc/rc.d/init.d/ntp stop >&2
	fi
	/sbin/chkconfig --del ntp
fi

%files
%defattr(644,root,root,755)
%doc conf/*.gz *.gz
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/ntp
%attr(640,root,root) %config %verify(not size md5 mtime) /etc/sysconfig/*
%{_mandir}/man8/*

%files doc-html
%defattr(644,root,root,755)
%doc html/*
