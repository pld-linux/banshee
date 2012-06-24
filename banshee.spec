# ToDo:
#	- make some proper bconds for other it
#
%include /usr/lib/rpm/macros.mono
#

Summary:	A Mono/GStreamer Based Music Player
Summary(pl):	Oparty na Mono/GStreamerze odtwarzacz muzyki
Name: 		banshee
Version: 	0.10.12
Release: 	0.1
License: 	GPL
Group:		Applications/Multimedia
Source0: 	http://banshee-project.org/files/banshee/%{name}-%{version}.tar.gz
# Source0-md5:	13806b7dee6444013dcb1436b4cf0e78
URL: 		http://banshee-project.org/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
BuildRequires:	dbus-devel >= 0.60
BuildRequires:	dotnet-avahi-devel
BuildRequires:	dotnet-dbus-sharp-devel
BuildRequires:	dotnet-gtk-sharp2-devel >= 2.8.0
BuildRequires:	dotnet-gnome-sharp-devel >= 2.8.0
BuildRequires:	gnome-desktop-devel
BuildRequires:	gstreamer-cdparanoia
BuildRequires:	gstreamer-devel >= 0.10.3
BuildRequires:	gstreamer-gnomevfs
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.3
BuildRequires:	gtk+2-devel >= 2.8.0
BuildRequires:	hal-devel >= 0.5.2
BuildRequires:	intltool >= 0.21
BuildRequires:	libtool
BuildRequires:	libmusicbrainz-devel >= 2.1.1
BuildRequires:	mono-csharp >= 1.1.13
BuildRequires:	monodoc
BuildRequires:	nautilus-cd-burner-devel >= 2.12.0
BuildRequires:	pkgconfig
BuildRequires:	sqlite3-devel
Requires:	gstreamer-cdparanoia >= 0.10.3
Requires:	gstreamer-gnomevfs >= 0.10.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Banshee is a brand spankin' new audio player based on the GStreamer
media library and is developed on the Open Source Mono .NET Platform,
written in C#.

%description -l pl
Banshee to nowy odtwarzacz d�wi�ku oparty na bibliotece odtwarzacza
multimedi�w GStreamer, rozwijany na platformie .NET Mono, napisany w
C#.

%prep
%setup -q

%build
%{__aclocal}
%{__libtoolize}
%{__automake}
%{__autoconf}
%configure \
	--disable-dev-tests \
	--disable-helix \
	--disable-ipod \
	--disable-njb \
	--disable-vlc \
	--enable-gstreamer \
	--enable-avahi \
	--disable-schemas-install
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/monodoc/sources

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_docdir}/%{name}/* $RPM_BUILD_ROOT%{_libdir}/monodoc/sources

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.{la,a}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:
SCHEMAS="banshee.schemas banshee-notificationareaicon.schemas audioscrobbler.schemas daap.schemas metadatasearch.schemas mmkeys.schemas"
for S in $SCHEMAS; do
	%gconf_schema_install $S
done

%preun
SCHEMAS="banshee.schemas banshee-notificationareaicon.schemas audioscrobbler.schemas daap.schemas metadatasearch.schemas mmkeys.schemas"
for S in $SCHEMAS; do
	%gconf_schema_install $S
done

%postun
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README 
%{_sysconfdir}/gconf/schemas/daap.schemas
%{_sysconfdir}/gconf/schemas/metadatasearch.schemas
%{_sysconfdir}/gconf/schemas/banshee.schemas
%{_sysconfdir}/gconf/schemas/banshee-notificationareaicon.schemas
%{_sysconfdir}/gconf/schemas/audioscrobbler.schemas
%{_sysconfdir}/gconf/schemas/mmkeys.schemas
%attr(755,root,root) %{_bindir}/banshee
%{_pkgconfigdir}/banshee.pc
%dir %{_libdir}/banshee
%{_libdir}/banshee/*.dll
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
