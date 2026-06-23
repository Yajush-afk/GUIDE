module com.guide.desktop {
    // The app uses JavaFX controls and layouts built directly in Java code.
    requires javafx.controls;

    // Exports the application package so the JavaFX launcher can start GuideApp.
    exports com.guide.desktop;
}
