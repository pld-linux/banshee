
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
Name: 		banshee
Version: 	0.10.8
Release: 	1
License: 	GPL
Group: 		Applications/Multimedia
Source: 	http://banshee-project.org/files/banshee/%{name}-%{version}.tar.gz
Patch0:		%{name}-stat.patch
URL: 		http://banshee.aaronbock.net
BuildRequires:	dbus-devel >= %{dbus_version}
BuildRequires:	gnome-desktop-devel >= 2.0
BuildRequires:	gst-sharp >= %{gst-sharp_version}
BuildRequires:	gstreamer-GConf >= 0.8
BuildRequires:	gstreamer-cdparanoia >= 0.8
BuildRequires:	gstreamer-devel >= %{gstreamer_version}
BuildRequires:	gstreamer-gnomevfs >= 0.8	
BuildRequires:	gstreamer-plugins-devel >= %{gstreamer-plugins_version}
BuildRequires:	gtk-sharp2-gapi >= %{gtk-sharp2_version}
BuildRequires:	hal-devel >= %{hal_version}
BuildRequires:	ipod-sharp >= %{ipod_version}
BuildRequires:	mono-data-sqlite >= %{mono_version}
BuildRequires:	mono-devel >= %{mono_version}
BuildRequires:	monodoc
BuildRequires:	nautilus-cd-burner-devel >= %{nautilus_version}
BuildRequires:	njb-sharp-devel
BuildRequires:	sqlite-devel >= %{sqlite_version}
Requires:	dbus >= %{dbus_version}
Requires:	dbus-sharp >= %{dbus_version}
Requires:	gst-sharp >= %{gst-sharp_version}
Requires:	gstreamer >= %{gstreamer_version}
Requires:	gstreamer-plugins >= %{gstreamer-plugins_version}
Requires:	gtk-sharp2 >= %{gtk-sharp2_version}
Requires:	ipod-sharp >= %{ipod_version}
Requires:	mono-data-sqlite >= %{mono_version}
Requires:	njb-sharp
Requires:	sqlite >= %{sqlite_version}
Requires: 	mono >= %{mono_version}
Obsoletes:	sonance <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Banshee is a brand spankin' new audio player based on the GStreamer
media library and is developed on the Open Source Mono .NET Platform,
written in C#.

%description -l pl
Banshee to nowy odtwarzacz d¼wiêku oparty na bibliotece odtwarzacza
multimediów GStreamer, rozwijany na platformie .NET Mono, napisany w
C#.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-daap \
	--disable-dev-tests \
	--disable-helix
	--disable-ipod \
	--disable-njb \
	--disable-vlc \
	--disable-xing
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
%find_lang %{name}

DESKTOPS="banshee.desktop"
for D in $DESKTOPS; do
	desktop-file-install --vendor %{desktop_vendor} \
	--dir $RPM_BUILD_ROOT%{_desktopdir}	\
	--add-category X-Red-Hat-Base	\
	--add-category Application	\
	--add-category AudioVideo	\
	$RPM_BUILD_ROOT%{_desktopdir}/$D
	mv $RPM_BUILD_ROOT%{_desktopdir}/%{desktop_vendor}-$D $RPM_BUILD_ROOT%{_desktopdir}/$D
done

rm -rf $RPM_BUILD_ROOT/var/scrollkeeper
find $RPM_BUILD_ROOT -name "*.la" -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database %{_desktopdir}
SCHEMAS="banshee.schemas audioscrobbler.schemas filesystemmonitor.schemas metadatasearch.schemas mmkeys.schemas"
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
for S in $SCHEMAS; do
	gconftool-2 \
	--makefile-install-rule \
	%{_sysconfdir}/gconf/schemas/$S > /dev/null || :
done

%postun
update-desktop-database %{_desktopdir}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README 
%{_sysconfdir}/gconf/schemas/filesystemmonitor.schemas
%{_sysconfdir}/gconf/schemas/metadatasearch.schemas
%{_sysconfdir}/gconf/schemas/banshee.schemas
%{_sysconfdir}/gconf/schemas/audioscrobbler.schemas
%{_sysconfdir}/gconf/schemas/mmkeys.schemas
%attr(755,root,root) %{_bindir}/banshee
%{_pkgconfigdir}/banshee.pc
%dir %{_libdir}/banshee
%{_libdir}/banshee/*.dll
#%{_libdir}/banshee/*.a
%attr(755,root,root) %{_libdir}/banshee/*.so
%{_libdir}/banshee/*.exe
%{_libdir}/banshee/*.mdb
%{_libdir}/banshee/*.config
#%{_libdir}/banshee/Banshee.Dap
%{_libdir}/banshee/Banshee.MediaEngine
%{_libdir}/banshee/Banshee.Plugins
%{_desktopdir}/banshee.desktop
%{_iconsdir}/hicolor/*/*/*
%{_datadir}/dbus-1/services/org.gnome.Banshee.service

%changelog
* %{date} PLD Team <feedback@pld-linux.org>
All persons listed below can be reached at <cvs_login>@pld-linux.org

$Log: banshee.spec,v $
Revision 1.2  2006-03-21 20:27:43  qboosh
- pl, some cleanups

Revision 1.1  2006/03/20  czarny
- init PLD spec
- adaptized from some strange rpm found out there in the net
- more to do, then done
- NFY
- builds and installs only with --nodeps

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
