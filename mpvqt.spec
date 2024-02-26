#
# Conditional build:
%bcond_with	tests		# build with tests
#
# TODO:
# - runtime Requires if any

%define		qtver		5.15.2
%define		kfname		mpvqt
Summary:	A libmpv wrapper for Qt Quick 2/Qml
Name:		mpvqt
Version:	1.0.0
Release:	1
License:	BSD 2/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://github.com/KDE/mpvqt/archive/refs/tags/v%{version}.tar.gz
# Source0-md5:	bed6b81b7df54e32da92d074aa18c9fa
URL:		http://invent.kde.org/libraries/mpvqt
BuildRequires:	Qt6Quick-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	kf6-extra-cmake-modules >= 5.102.0
BuildRequires:	mpv-client-devel
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MpvQt is a [libmpv](https://github.com/mpv-player/mpv/) wrapper for Qt
Quick 2/Qml.

%package devel
Summary:	Header files for %{name} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{name}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{name}.

%prep
%setup -q

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=5
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libMpvQt.so.1
%attr(755,root,root) %{_libdir}/libMpvQt.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/MpvQt
%{_libdir}/cmake/MpvQt
%{_libdir}/libMpvQt.so
