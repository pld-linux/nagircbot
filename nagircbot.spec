Summary:	NagIRCBot - announce the Nagios status on an IRC channel
Summary(pl.UTF-8):	NagIRCBot - pokazywanie statusu Nagiosa na kanale IRC
Name:		nagircbot
Version:	0.0.33
Release:	2
License:	GPL
Group:		Applications
Source0:	http://www.vanheusden.com/nagircbot/%{name}-%{version}.tgz
# Source0-md5:	8dd1f2077d91ca9273d92a3b207c54b2
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
	LDFLAGS="%{rpmldflags} -lstdc++ -lssl -lcrypto"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/rc.d/init.d,/etc/sysconfig}

cp -a %{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}
cp -a %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

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
