%define name		banshee
%define version		0.10.8
%define release		1%{?dist}
%define	cflags		--disable-njb --disable-ipod --disable-dev-tests --disable-vlc --disable-xing --disable-daap --disable-helix

%define	mono_version			1.1.10
%define gstreamer_version		0.8.6
%define	gstreamer-plugins_version	0.8.6
%define	gtk2-sharp_version		2.4.0
%define	gst-sharp_version		0.2.0
%define	sqlite_version			3.2.8
%define	ipod_version			0.5.2
%define	dbus_version			0.50
%define	hal_version			0.5.2
%define nautilus_version		2.12.1

Summary:	A Mono/GStreamer Based Music Player
Summary(pl):	Oparty na Mono/GStreamerze odtwarzacz muzyki
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Applications/Multimedia
Source: 	http://banshee-project.org/files/%{name}/%{name}-%{version}.tar.gz
Patch0:		%{name}-stat.patch
URL: 		http://banshee.aaronbock.net
BuildRoot: 	%{_tmppath}/%{name}-%{version}
Obsoletes:	sonance <= %{version}
Requires: 	mono >= %{mono_version}
Requires:	gstreamer >= %{gstreamer_version}
Requires:	gstreamer-plugins >= %{gstreamer-plugins_version}
Requires:	gtk-sharp2 >= %{gtk-sharp2_version}
Requires:	gst-sharp >= %{gst-sharp_version}
Requires:	mono-data-sqlite >= %{mono_version}
Requires:	ipod-sharp >= %{ipod_version}
Requires:	dbus-sharp >= %{dbus_version}
Requires:	dbus >= %{dbus_version}
Requires:	sqlite >= %{sqlite_version}
Requires:	njb-sharp
BuildRequires:	mono-devel >= %{mono_version}
BuildRequires:	gstreamer-devel >= %{gstreamer_version}
BuildRequires:	gstreamer-plugins-devel >= %{gstreamer-plugins_version}
BuildRequires:	gtk-sharp2-gapi >= %{gtk-sharp2_version}
BuildRequires:	gstreamer-cdparanoia >= 0.8
BuildRequires:	gstreamer-gnomevfs >= 0.8	
BuildRequires:	gstreamer-GConf >= 0.8
BuildRequires:	gnome-desktop-devel >= 2.0
BuildRequires:	gst-sharp >= %{gst-sharp_version}
BuildRequires:	ipod-sharp >= %{ipod_version}
BuildRequires:	dbus-devel >= %{dbus_version}
BuildRequires:	hal-devel >= %{hal_version}
BuildRequires:	monodoc
BuildRequires:	mono-data-sqlite >= %{mono_version}
BuildRequires:	nautilus-cd-burner-devel >= %{nautilus_version}
BuildRequires:	sqlite-devel >= %{sqlite_version}
BuildRequires:	njb-sharp-devel

%description
Banshee is a brand spankin' new audio player based on the GStreamer 
media library and is developed on the Open Source Mono .NET Platform, 
written in C#.

%prep
%setup -q
%patch0 -p1

%build
%configure %{cflags}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT%{_datadir}/applications

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
%find_lang %{name}

DESKTOPS="banshee.desktop"
for D in $DESKTOPS; do
	desktop-file-install --vendor %{desktop_vendor} \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications	\
	--add-category X-Red-Hat-Base	\
	--add-category Application	\
	--add-category AudioVideo	\
	$RPM_BUILD_ROOT%{_datadir}/applications/$D
	mv $RPM_BUILD_ROOT%{_datadir}/applications/%{desktop_vendor}-$D $RPM_BUILD_ROOT%{_datadir}/applications/$D
done

rm -rf $RPM_BUILD_ROOT/var/scrollkeeper
find $RPM_BUILD_ROOT -name "*.la" -exec rm {} \;

%post
update-desktop-database %{_datadir}/applications
SCHEMAS="banshee.schemas audioscrobbler.schemas filesystemmonitor.schemas metadatasearch.schemas mmkeys.schemas"
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
for S in $SCHEMAS; do
	gconftool-2 \
	--makefile-install-rule \
	%{_sysconfdir}/gconf/schemas/$S > /dev/null || :
done

%postun
update-desktop-database %{_datadir}/applications

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README 
%{_sysconfdir}/gconf/schemas/filesystemmonitor.schemas
%{_sysconfdir}/gconf/schemas/metadatasearch.schemas
%{_sysconfdir}/gconf/schemas/banshee.schemas
%{_sysconfdir}/gconf/schemas/audioscrobbler.schemas
%{_sysconfdir}/gconf/schemas/mmkeys.schemas
%{_bindir}/banshee
%{_libdir}/pkgconfig/banshee.pc
%{_libdir}/banshee/*.dll
%{_libdir}/banshee/*.a
%{_libdir}/banshee/*.so
%{_libdir}/banshee/*.exe
%{_libdir}/banshee/*.mdb
%{_libdir}/banshee/*.config
#%{_libdir}/banshee/Banshee.Dap/
%{_libdir}/banshee/Banshee.MediaEngine/
%{_libdir}/banshee/Banshee.Plugins/
%{_datadir}/applications/banshee.desktop
%{_datadir}/icons/hicolor/
%{_datadir}/dbus-1/services/org.gnome.Banshee.service

%changelog
* Tue Feb 07 2006 Matthew Hall <matt@nrpms.net> 0.10.5-1
- 0.10.5 Release

* Wed Feb 01 2006 Matthew Hall <matt@nrpms.net> 0.10.4-2
- Enable njb support

* Wed Jan 18 2006 Matthew Hall <matt@nrpms.net> 0.10.4-1
- 0.10.4 Release

* Tue Jan 03 2006 Matthew Hall <matt@nrpms.net> 0.10.2-1
- 0.10.2 Release

* Wed Dec 07 2005 Matthew Hall <matt@nrpms.net> 0.10-1
- 0.10 Release

* Sat Nov 12 2005 Matthew Hall <matt@nrpms.net> 0.9.11.1-1
- 0.9.11.1 Release

* Thu Nov 10 2005 Matthew Hall <matt@nrpms.net> 0.9.11-1
- 0.9.11 Release

* Mon Sep 26 2005 Matthew Hall <matt@nrpms.net> 0.9.7.1-2
- R/BR: 's/gtk-sharp/gtk-sharp2/'

* Fri Sep 16 2005 Matthew Hall <matt@nrpms.net> 0.9.7.1-1
- 0.9.7.1 Release

* Mon Aug 29 2005 Matthew Hall <matt@nrpms.net> 0.8.7.1-1
- 0.8.7.1 Release

* Tue Aug 16 2005 Matthew Hall <matt@nrpms.net> 0.8.3-1
- 0.8.3 Release
- Sonance renamed to Banshee

* Tue Aug 02 2005 Matthew Hall <matt@nrpms.net> 0.8.0-1
- 0.8.0 Release

* Thu Jul 28 2005 Matthew Hall <matt@nrpms.net> 0.7.3-1
- 0.2.1 Release
