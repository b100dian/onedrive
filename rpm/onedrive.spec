#
# spec file for package onedrive
#
# Copyright (c) 2021 SUSE LLC
# Copyright (c) 2018-2020 LISA GmbH, Bingen, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%define _unitdir /usr/lib/systemd/system
%{!?_userunitdir: %{expand: %%global _userunitdir %{_unitdir}/../user}}
%define docdir %{_defaultdocdir}/%{name}

# DMD is available only on x86*. Use LDC otherwise.
%ifarch %{ix86} x86_64
%bcond_without dcompiler_dmd
%else
%bcond_with dcompiler_dmd
%endif

Name:           onedrive
Version:        2.5.10
Release:        0
Summary:        Client for One Drive Service for Linux
License:        GPL-3.0-only
Group:          Productivity/Networking/Other
URL:            https://github.com/abraunegg/onedrive/
Source0:        %{name}-%{version}.tar.gz
%if %{with dcompiler_dmd}
BuildRequires:  dmd
BuildRequires:  phobos-devel-static
%else
BuildRequires:  ldc
#BuildRequires:  ldc-phobos-devel
%endif
Buildrequires:  dbus-devel
BuildRequires:  help2man
BuildRequires:  libcurl-devel
BuildRequires:  sqlite-devel
Recommends:     logrotate
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
OneDrive is a client for Microsoft file serving service

%prep
%setup -q
#sed -i /chown/d Makefile
sed -i 's/^docdir.*/docdir = @docdir@/g' Makefile.in

%build
%configure \
    --docdir=%{docdir} \
    --with-systemduserunitdir=%_userunitdir \
    --with-systemdsystemunitdir=%_unitdir \
    --enable-notifications

make %{?_smp_mflags} %{name}

%install
%make_install
install -D -m 0644 config %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -d -m 0755 %{buildroot}%{_localstatedir}/log/%{name}

%files
/usr/share/icons/hicolor/scalable/places/onedrive.svg
/usr/share/doc/onedrive/LICENSE
/usr/share/doc/onedrive/advanced-usage.md
/usr/share/doc/onedrive/application-config-options.md
/usr/share/doc/onedrive/application-security.md
/usr/share/doc/onedrive/business-shared-items.md
/usr/share/doc/onedrive/changelog.md
/usr/share/doc/onedrive/client-architecture.md
/usr/share/doc/onedrive/config
/usr/share/doc/onedrive/contributing.md
/usr/share/doc/onedrive/docker.md
/usr/share/doc/onedrive/install.md
/usr/share/doc/onedrive/known-issues.md
/usr/share/doc/onedrive/national-cloud-deployments.md
/usr/share/doc/onedrive/podman.md
/usr/share/doc/onedrive/privacy-policy.md
/usr/share/doc/onedrive/readme.md
/usr/share/doc/onedrive/server-side-filtering-limitations.md
/usr/share/doc/onedrive/sharepoint-libraries.md
/usr/share/doc/onedrive/terms-of-service.md
/usr/share/doc/onedrive/ubuntu-package-install.md
/usr/share/doc/onedrive/usage.md
/usr/share/doc/onedrive/webhooks.md
%defattr(-,root,root)
%license LICENSE
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/%{name}
%dir %{_userunitdir}
%{_userunitdir}/%{name}.service
%{_unitdir}/%{name}@.service
%attr(0644, root, root) %{_mandir}/man1/%{name}.1*
%{_localstatedir}/log/%{name}


%changelog
