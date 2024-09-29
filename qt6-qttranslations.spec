# No code here...
# But can't make it noarch because of lib vs. lib64
%define debug_package %{nil}

#define beta rc2
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qttranslations
Version:	6.7.3
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qttranslations.git
Source:		qttranslations-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qttranslations-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Translations
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt%{major}Core)
BuildRequires:	cmake(Qt%{major}Linguist)
BuildRequires:	cmake(Qt%{major}LinguistTools)
BuildRequires:	qt%{major}-cmake
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} Translations

%files -f core.lang
%{_qtdir}/translations/catalogs.json

%package assistant
Summary: Translations for Qt Assistant
Requires: qt%{major}-qttools-assistant = %{version}
Supplements: qt%{major}-qttools-assistant

%description assistant
Translations for Qt Assistant

%files assistant -f assistant.lang

%package designer
Summary: Translations for Qt Designer
Requires: qt%{major}-qttools-designer = %{version}
Supplements: qt%{major}-qttools-designer

%description designer
Translations for Qt Designer

%files designer -f designer.lang

%package linguist
Summary: Translations for Qt Linguist
Requires: qt%{major}-qttools-linguist = %{version}
Supplements: qt%{major}-qttools-linguist

%description linguist
Translations for Qt Linguist

%files linguist -f linguist.lang

%package connectivity
Summary: Translations for Qt Connectivity
Requires: %{_lib}Qt%{major}Bluetooth = %{version}
Requires: %{_lib}Qt%{major}Nfc = %{version}
Supplements: %{_lib}Qt%{major}Bluetooth
Supplements: %{_lib}Qt%{major}Nfc

%description connectivity
Translations for Qt Connectivity

%files connectivity -f qtconnectivity.lang

%package declarative
Summary: Translations for Qt Declarative
Requires: %{_lib}Qt%{major}Qml = %{version}
Supplements: %{_lib}Qt%{major}Qml

%description declarative
Translations for Qt Declarative

%files declarative -f qtdeclarative.lang

%package location
Summary: Translations for Qt Location
Requires: %{_lib}Qt%{major}Location = %{version}
Supplements: %{_lib}Qt%{major}Location

%description location
Translations for Qt Location

%files location -f qtlocation.lang

%package multimedia
Summary: Translations for Qt Multimedia
Requires: %{_lib}Qt%{major}Multimedia = %{version}
Supplements: %{_lib}Qt%{major}Multimedia

%description multimedia
Translations for Qt Multimedia

%files multimedia -f qtmultimedia.lang

%package serialport
Summary: Translations for Qt SerialPort
Requires: %{_lib}Qt%{major}SerialPort = %{version}
Supplements: %{_lib}Qt%{major}SerialPort

%description serialport
Translations for Qt SerialPort

%files serialport -f qtserialport.lang

%package webengine
Summary: Translations for Qt WebEngine
Requires: %{_lib}Qt%{major}WebEngine = %{version}
Supplements: %{_lib}Qt%{major}WebEngine

%description webengine
Translations for Qt WebEngine

%files webengine -f qtwebengine.lang

%package websockets
Summary: Translations for Qt WebSockets
Requires: %{_lib}Qt%{major}WebSockets = %{version}
Supplements: %{_lib}Qt%{major}WebSockets

%description websockets
Translations for Qt WebSockets

%files websockets -f qtwebsockets.lang

%prep
%autosetup -p1 -n qttranslations%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
TOP="$(pwd)"
%ninja_install -C build
cd %{buildroot}%{_qtdir}/translations
for i in *.qm; do
	if echo $i |grep -qE '^(qt_help)'; then
		PROJECT=$(echo $i |cut -d_ -f1-2)
		LNG=$(basename $i .qm |cut -d_ -f3-)
	else
		PROJECT=$(echo $i |cut -d_ -f1)
		LNG=$(basename $i .qm|cut -d_ -f2-)
	fi
	echo "%%lang($LNG) %{_qtdir}/translations/$i" >>${TOP}/$PROJECT.lang
done
cd -
cat qtbase.lang qt_help.lang qt.lang >core.lang
%qt6_postinstall
