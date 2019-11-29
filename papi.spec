Name:            papi
Version:         5.6.0
Release:         8
Summary:         Performance Application Programming Interface
License:         BSD
URL:             http://icl.cs.utk.edu/papi/
Source0:         http://icl.cs.utk.edu/projects/papi/downloads/%{name}-%{version}.tar.gz
BuildRequires:   autoconf doxygen ncurses-devel gcc-gfortran kernel-headers >= 2.6.32
BuildRequires:   chrpath lm_sensors-devel libpfm-devel >= 4.6.0-1 libpfm-static >= 4.6.0-1
BuildRequires:   net-tools rdma-core-devel infiniband-diags-devel perl-generators
Provides:        papi-libs = %{version}-%{release}
Obsoletes:       papi-libs < %{version}-%{release}

Patch0001:       papi-ldflags.patch

%description
PAPI provides a programmer interface to monitor the performance of
running programs,and contains the run-time libraries for any application that wishes
to use PAPI.

%package         devel
Summary:         Header files for the compiling programs with PAPI
Requires:        papi = %{version}-%{release} pkgconfig
Provides:        papi-testsuite = %{version}-%{release} papi-static = %{version}-%{release}
Obsoletes:       papi-testsuite < %{version}-%{release} papi-static < %{version}-%{release}

%description     devel
PAPI-devel provides C header files for specifying PAPI user-space libraries and interfaces,
a test testuiste for checking PAPI functionality, and static libraries for compiling programs with PAPI.

%package        help
Summary:        Help documents for papi

%description    help
The papi-help package conatins manual pages and documents for papi.

%prep
%autosetup -p1

%build
cd src
autoconf
%configure --with-perf-events --with-pfm-incdir=%{_includedir} --with-pfm-libdir=%{_libdir} \
--with-static-lib=yes --with-shared-lib=yes --with-shlib --with-shlib-tools \
--with-components="appio coretemp example infiniband lmsensors lustre micpower mx net rapl stealtime"

cd components
cd infiniband_umad; %configure
cd ../lmsensors; %configure --with-sensors_incdir=/usr/include/sensors  --with-sensors_libdir=%{_libdir};
cd ../../

DBG="" make %{?_smp_mflags}
cd ../doc
DBG="" make
DBG="" make install

%install
cd src
make DESTDIR=$RPM_BUILD_ROOT LDCONFIG=/bin/true install-all

chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so*

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc LICENSE.txt
%{_bindir}/*
%{_libdir}/*.so.*
%dir /usr/share/papi
/usr/share/papi/papi_events.csv

%files devel
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/papi*.pc
%{_libdir}/*.a
/usr/share/papi/*
%exclude /usr/share/papi/papi_events.csv

%files help
%doc INSTALL.txt README RELEASENOTES.txt
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Thu Nov 28 2019 liujing<liujing144@huawei.com> - 5.6.0-8
- Package init
