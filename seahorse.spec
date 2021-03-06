Summary:	GNOME application for managing encryption keys
Name:		seahorse
Version:	3.14.0
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/seahorse/3.14/%{name}-%{version}.tar.xz
# Source0-md5:	1c54bb9030ff054b870d79e86b91de6b
URL:		http://www.gnome.org/projects/seahorse/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	gcr-devel >= 3.14.0
BuildRequires:	gettext-devel
BuildRequires:	gnupg
BuildRequires:	gobject-introspection-devel >= 1.42.0
BuildRequires:	gpgme-devel
BuildRequires:	intltool
BuildRequires:	libnotify-devel
BuildRequires:	libsoup-devel
BuildRequires:	libtool
BuildRequires:	openldap-devel
BuildRequires:	pkg-config
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	gtk+-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	gcr >= 3.14.0
Requires:	gnome-keyring >= 3.14.0
Requires:	gnupg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/seahorse

%description
Seahorse is a GNOME application for managing encryption keys
and passwords in the GnomeKeyring

%package shell-search-provider
Summary:	GNOME Shell search provider
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gnome-shell

%description shell-search-provider
Search result provider for GNOME Shell.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	SSH_KEYGEN_PATH=%{_bindir}/ssh-keygen	\
	SSH_PATH=%{_bindir}/ssh			\
	--disable-schemas-compile 		\
	--disable-silent-rules			\
	--disable-static			\
	--enable-pgp
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/GConf
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_icon_cache hicolor
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/seahorse
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/seahorse-ssh-askpass
%attr(755,root,root) %{_libexecdir}/xloadimage
%{_datadir}/%{name}
%{_datadir}/dbus-1/services/org.gnome.seahorse.Application.service
%{_datadir}/glib-2.0/schemas/org.gnome.seahorse.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.seahorse.manager.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.seahorse.window.gschema.xml
%{_desktopdir}/seahorse.desktop
%{_iconsdir}/hicolor/*/*/*
%{_mandir}/man1/seahorse.1*

%files shell-search-provider
%defattr(644,root,root,755)
%{_datadir}/gnome-shell/search-providers/seahorse-search-provider.ini

