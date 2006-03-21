# ToDo:
#	- check Patch0
#	- make avahi.pc work (propable bug in avahi package,
#		it doesn't make a proper symlink for the .dll
#	- make some proper bconds for other it
#
%include /usr/lib/rpm/macros.mono
#

Summary:	A Mono/GStreamer Based Music Player
Summary(pl):	Oparty na Mono/GStreamerze odtwarzacz muzyki
Name: 		banshee
Version: 	0.10.8
Release: 	0.1
License: 	GPL
Group: 		Applications/Multimedia
Source0: 	http://banshee-project.org/files/banshee/%{name}-%{version}.tar.gz
# Source0-md5:	cfa4051cd8aba171a09dcb9a3f34fef3
Patch0:		%{name}-stat.patch
URL: 		http://banshee-project.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	avahi-compat-howl-devel
BuildRequires:	dotnet-avahi-devel
BuildRequires:	dotnet-dbus-sharp-devel
BuildRequires:	dotnet-gtk-sharp2-devel >= 2.3.92
BuildRequires:	gnome-desktop-devel
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.0
BuildRequires:	hal-devel >= 0.5.2
BuildRequires:	libtool
BuildRequires:	libmusicbrainz-devel
BuildRequires:	mono-csharp >= 1.1.10
BuildRequires:	monodoc
BuildRequires:	nautilus-cd-burner-devel >= 2.12.0
BuildRequires:	pkgconfig
BuildRequires:	sqlite3-devel
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
#%patch0 -p1

%build
%configure \
	--disable-daap \
	--disable-dev-tests \
	--disable-helix \
	--disable-ipod \
	--disable-njb \
	--disable-vlc \
	--disable-xing \
	--with-gstreamer-0-10
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:
SCHEMAS="banshee.schemas banshee-notificationareaicon.schemas audioscrobbler.schemas filesystemmonitor.schemas metadatasearch.schemas mmkeys.schemas"
for S in $SCHEMAS; do
	%gconf_schema_install $S
done

%preun
SCHEMAS="banshee.schemas banshee-notificationareaicon.schemas audioscrobbler.schemas filesystemmonitor.schemas metadatasearch.schemas mmkeys.schemas"
for S in $SCHEMAS; do
	%gconf_schema_install $S
done

%postun
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README 
%{_sysconfdir}/gconf/schemas/filesystemmonitor.schemas
%{_sysconfdir}/gconf/schemas/metadatasearch.schemas
%{_sysconfdir}/gconf/schemas/banshee.schemas
%{_sysconfdir}/gconf/schemas/banshee-notificationareaicon.schemas
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
%{_libdir}/monodoc/sources/*
%{_desktopdir}/banshee.desktop
%{_iconsdir}/hicolor/*/*/*
%{_datadir}/dbus-1/services/org.gnome.Banshee.service
