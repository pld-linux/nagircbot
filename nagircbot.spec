Summary:	NagIRCBot - announce the Nagios status on an IRC channel
Summary(pl.UTF-8):	NagIRCBot - pokazywanie statusu Nagiosa na kanale IRC
Name:		nagircbot
Version:	0.0.30
Release:	2
License:	GPL
Group:		Applications
Source0:	http://www.vanheusden.com/nagircbot/%{name}-%{version}.tgz
# Source0-md5:	deecd1752ce86ec90f7d5ce17988ed21
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-nodebug.patch
URL:		http://www.vanheusden.com/nagircbot/
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NagIRCBot announces the Nagios status on an IRC channel.

%description -l pl.UTF-8
NagIRCBot pokazuje status Nagiosa na kanale IRC.

%prep
%setup -q
%patch0 -p0

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	DEBUG="%{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags} -lstdc++ -lssl"

%install
rm -rf $RPM_BUILD_ROOT

install -D %{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}
install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "Nagios IRC Bot"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc readme.txt
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/nagircbot
%attr(755,root,root) %{_sbindir}/nagircbot
%attr(754,root,root) /etc/rc.d/init.d/nagircbot
