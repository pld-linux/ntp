Summary:	Network Time Protocol utilities
Summary(pl):	Narzêdzia do synchronizacji czasu (Network Time Protocol)
Name:		ntp
Version:	4.0.99k
Release:	1
Copyright:	distributable
Group:		Daemons
Group(pl):	Serwery
Source0:	ftp://ftp.udel.edu/pub/ntp/%{name}-%{version}.tar.gz
Source1:	ntp.conf
Source2:	ntp.keys
Source3:	ntp.rc
Source4:	ntp.sysconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ntp
%define		_bindir		%{_sbindir}
%define		_prefix		/usr

%description
This package contains utilities and daemons to help synchronize your
computer's time to UTC standard time. It includes ntpdate, a program
similar to rdate, and xntpd, a daemon which adjusts the system time
continuously.

%description -l pl
Pakiet zawiera narzêdzia i demony s³u¿±ce do dok³adnego synchronizowania
czasu Twojego komputera: ntpdate, program podobny do rdatei xntpd, 
demon aktualizuj±cy czas w sposób ci±g³y.

%prep 
%setup -q

%build
LDFLAGS="-s"; export LDFLAGS

echo "y" | ./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir} --bindir=%{_bindir}

%{__make} 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{ntp,rc.d/init.d,sysconfig}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/ntp/ntp.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/ntp/keys
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/ntp
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/ntp

gzip -9fn NEWS TODO conf/*.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ntp

if [ -f /var/lock/subsystem/ntp ]; then
	/etc/rc.d/init.d/ntp restart >&2
else
	echo "Run \"/etc/rc.d/init.d/ntp start\" to start ntp daemon."
fi
    
%preun
if [ $1 = 0 ]; then
	/sbin/chkconfig --del ntp
	/etc/rc.d/init.d/ntp stop >&2
fi

%files
%defattr(644,root,root,755)
%doc conf/*.gz *.gz

%attr(750,root,root) %dir /etc/ntp
%attr(640,root,root) %config(noreplace) %verify(not size md5 mtime) /etc/ntp/*
%attr(640,root,root) %config %verify(not size md5 mtime) /etc/sysconfig/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/ntp
