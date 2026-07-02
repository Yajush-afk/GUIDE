package com.guide.desktop;

import javafx.animation.FadeTransition;
import javafx.animation.Interpolator;
import javafx.animation.ParallelTransition;
import javafx.animation.Timeline;
import javafx.animation.KeyFrame;
import javafx.animation.KeyValue;
import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.ScrollPane;
import javafx.scene.control.Separator;
import javafx.scene.control.ToggleButton;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.scene.layout.Region;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import javafx.util.Duration;

import java.util.List;

public final class GuideApp extends Application {
    private static final double WINDOW_WIDTH = 1120;
    private static final double WINDOW_HEIGHT = 680;
    private static final double LEFT_EXPANDED_WIDTH = 260;
    private static final double RIGHT_EXPANDED_WIDTH = 240;
    private static final double COLLAPSED_WIDTH = 68;
    private static final Duration PANEL_ANIMATION_TIME = Duration.millis(240);
    private static final Duration TEXT_FADE_TIME = Duration.millis(110);

    private final List<String> tutorials = List.of(
            "How to Use File Explorer",
            "How to Open a Website"
    );

    private VBox leftSidebar;
    private VBox rightSidebar;
    private VBox tutorialList;
    private VBox settingsList;
    private ScrollPane tutorialScrollPane;
    private Label leftSidebarTitle;
    private Label rightSidebarTitle;
    private StackPane appRoot;
    private StackPane contentHost;
    private boolean leftCollapsed;
    private boolean rightCollapsed;
    private TutorialOverlay tutorialOverlay;
    private boolean darkMode;
    private double dragOffsetX;
    private double dragOffsetY;

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage stage) {
        stage.initStyle(StageStyle.TRANSPARENT);

        StackPane root = buildAppShell(stage);
        Scene scene = new Scene(root, WINDOW_WIDTH, WINDOW_HEIGHT);
        scene.setFill(Color.TRANSPARENT);
        scene.getStylesheets().add(getClass().getResource("/guide-app.css").toExternalForm());

        stage.setTitle("Guide");
        stage.setScene(scene);
        stage.setMinWidth(860);
        stage.setMinHeight(560);
        stage.show();

        playFadeIn(root);
    }

    private StackPane buildAppShell(Stage stage) {
        leftSidebar = buildLeftSidebar();
        rightSidebar = buildRightSidebar();
        contentHost = new StackPane(buildGreetingView());
        contentHost.getStyleClass().add("content-host");

        BorderPane layout = new BorderPane();
        layout.setLeft(leftSidebar);
        layout.setCenter(contentHost);
        layout.setRight(rightSidebar);

        VBox shell = new VBox(buildTitleBar(stage), layout);
        VBox.setVgrow(layout, Priority.ALWAYS);

        StackPane appFrame = new StackPane(shell);
        appFrame.getStyleClass().add("app-frame");

        tutorialOverlay = new TutorialOverlay();

        // Add appFrame first, then the overlay on top.
        appRoot = new StackPane(appFrame, tutorialOverlay);
        appRoot.getStyleClass().add("window-root");
        return appRoot;
    }

    private HBox buildTitleBar(Stage stage) {
        Label appName = new Label("GUIDE");
        appName.getStyleClass().add("titlebar-brand");

        Label appSubtitle = new Label("Learning overlay");
        appSubtitle.getStyleClass().add("titlebar-subtitle");

        HBox titleGroup = new HBox(10, appName, appSubtitle);
        titleGroup.setAlignment(Pos.CENTER_LEFT);

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);

        Button themeButton = buildWindowButton("☾");
        themeButton.getStyleClass().add("theme-button");
        themeButton.setOnAction(event -> toggleDarkMode(themeButton));

        Button minimizeButton = buildWindowButton("−");
        minimizeButton.setOnAction(event -> stage.setIconified(true));

        Button maximizeButton = buildWindowButton("□");
        maximizeButton.setOnAction(event -> {
            stage.setMaximized(!stage.isMaximized());
            maximizeButton.setText(stage.isMaximized() ? "❐" : "□");
        });

        Button closeButton = buildWindowButton("×");
        closeButton.getStyleClass().add("window-close-button");
        closeButton.setOnAction(event -> stage.close());

        HBox titleBar = new HBox(8, titleGroup, spacer, themeButton, minimizeButton, maximizeButton, closeButton);
        titleBar.getStyleClass().add("titlebar");
        titleBar.setAlignment(Pos.CENTER_LEFT);
        titleBar.setOnMousePressed(event -> {
            dragOffsetX = event.getSceneX();
            dragOffsetY = event.getSceneY();
        });
        titleBar.setOnMouseDragged(event -> {
            if (!stage.isMaximized()) {
                stage.setX(event.getScreenX() - dragOffsetX);
                stage.setY(event.getScreenY() - dragOffsetY);
            }
        });
        titleBar.setOnMouseClicked(event -> {
            if (!(event.getTarget() instanceof Button) && event.getClickCount() == 2) {
                stage.setMaximized(!stage.isMaximized());
                maximizeButton.setText(stage.isMaximized() ? "❐" : "□");
            }
        });
        return titleBar;
    }

    private void toggleDarkMode(Button themeButton) {
        darkMode = !darkMode;
        themeButton.setText(darkMode ? "☀" : "☾");
        appRoot.getStyleClass().remove("dark");
        if (darkMode) {
            appRoot.getStyleClass().add("dark");
        }
    }

    private Button buildWindowButton(String text) {
        Button button = new Button(text);
        button.getStyleClass().add("window-button");
        button.setFocusTraversable(false);
        return button;
    }

    private VBox buildLeftSidebar() {
        leftSidebarTitle = new Label("Tutorials");
        leftSidebarTitle.getStyleClass().add("sidebar-title");

        Button collapseButton = new Button("<");
        collapseButton.getStyleClass().add("icon-button");
        collapseButton.setOnAction(event -> toggleLeftSidebar(collapseButton));

        HBox header = buildSidebarHeader(leftSidebarTitle, collapseButton);

        tutorialList = new VBox(8);
        tutorialList.getStyleClass().add("sidebar-section");

        // Each tutorial button updates the center pane without rebuilding the full shell.
        for (int index = 0; index < tutorials.size(); index++) {
            String tutorial = tutorials.get(index);
            Button tutorialButton = new Button(tutorial);
            tutorialButton.getStyleClass().add("tutorial-button");
            tutorialButton.setMaxWidth(Double.MAX_VALUE);
            tutorialButton.setOnAction(event -> showTutorialView(tutorial));
            tutorialList.getChildren().add(tutorialButton);
        }

        tutorialScrollPane = new ScrollPane(tutorialList);
        tutorialScrollPane.getStyleClass().add("sidebar-scroll");
        tutorialScrollPane.setFitToWidth(true);
        VBox.setVgrow(tutorialScrollPane, Priority.ALWAYS);

        VBox sidebar = new VBox(18, header, tutorialScrollPane);
        sidebar.getStyleClass().addAll("sidebar", "left-sidebar");
        sidebar.setPrefWidth(LEFT_EXPANDED_WIDTH);
        return sidebar;
    }

    private VBox buildRightSidebar() {
        rightSidebarTitle = new Label("Settings");
        rightSidebarTitle.getStyleClass().add("sidebar-title");

        Button collapseButton = new Button(">");
        collapseButton.getStyleClass().add("icon-button");
        collapseButton.setOnAction(event -> toggleRightSidebar(collapseButton));

        HBox header = buildSidebarHeader(rightSidebarTitle, collapseButton);

        settingsList = new VBox(12);
        settingsList.getStyleClass().add("sidebar-section");
        settingsList.getChildren().addAll(
                buildSettingToggle("API Key"),
                buildSettingToggle("Display settings"),
                buildSettingToggle("Large text"),
                new Separator(),
                buildPlaceholderText("More tutorial preferences can be added here.")
        );

        VBox sidebar = new VBox(18, header, settingsList);
        sidebar.getStyleClass().addAll("sidebar", "right-sidebar");
        sidebar.setPrefWidth(RIGHT_EXPANDED_WIDTH);
        return sidebar;
    }

    private HBox buildSidebarHeader(Label title, Button collapseButton) {
        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);

        HBox header = new HBox(10, title, spacer, collapseButton);
        header.setAlignment(Pos.CENTER_LEFT);
        header.getStyleClass().add("sidebar-header");
        return header;
    }

    private ToggleButton buildSettingToggle(String label) {
        ToggleButton toggle = new ToggleButton(label);
        toggle.getStyleClass().add("setting-toggle");
        toggle.setMaxWidth(Double.MAX_VALUE);
        return toggle;
    }

    private Label buildPlaceholderText(String text) {
        Label label = new Label(text);
        label.getStyleClass().add("placeholder-text");
        label.setWrapText(true);
        return label;
    }

    private VBox buildGreetingView() {
        Label eyebrow = new Label("Welcome back");
        eyebrow.getStyleClass().add("eyebrow");

        Label title = new Label("Choose a tutorial from the left panel");
        title.getStyleClass().add("hero-title");
        title.setWrapText(true);

        Label body = new Label("Your selected tutorial will open here with a start action and learning details.");
        body.getStyleClass().add("body-text");
        body.setWrapText(true);

        VBox view = new VBox(14, eyebrow, title, body);
        view.setAlignment(Pos.CENTER);
        view.setPadding(new Insets(48));
        view.getStyleClass().add("center-view");
        return view;
    }

    private VBox buildTutorialView(String tutorialName) {
        Label eyebrow = new Label("Selected tutorial");
        eyebrow.getStyleClass().add("eyebrow");

        Label title = new Label(tutorialName);
        title.getStyleClass().add("hero-title");
        title.setWrapText(true);

        Label body = new Label("This placeholder area is ready for lessons, notes, videos, or practice tasks.");
        body.getStyleClass().add("body-text");
        body.setWrapText(true);

        Button startButton = new Button("Start");
        startButton.getStyleClass().add("primary-button");

        VBox view = new VBox(16, eyebrow, title, body, startButton);
        view.setAlignment(Pos.CENTER);
        view.setPadding(new Insets(48));
        view.getStyleClass().add("center-view");
        return view;
    }

    private void showTutorialView(String tutorialName) {
        replaceCenterContent(buildTutorialView(tutorialName));
    }

    private void replaceCenterContent(VBox nextView) {
        // A short fade keeps pane changes visible without making navigation feel slow.
        FadeTransition fadeOut = new FadeTransition(Duration.millis(90), contentHost);
        fadeOut.setFromValue(1);
        fadeOut.setToValue(0);
        fadeOut.setOnFinished(event -> {
            contentHost.getChildren().setAll(nextView);
            FadeTransition fadeIn = new FadeTransition(Duration.millis(140), contentHost);
            fadeIn.setFromValue(0);
            fadeIn.setToValue(1);
            fadeIn.play();
        });
        fadeOut.play();
    }

    private void toggleLeftSidebar(Button collapseButton) {
        leftCollapsed = !leftCollapsed;
        collapseButton.setText(leftCollapsed ? ">" : "<");
        animateSidebarState(
                leftSidebar,
                leftSidebarTitle,
                tutorialScrollPane,
                leftCollapsed,
                leftCollapsed ? COLLAPSED_WIDTH : LEFT_EXPANDED_WIDTH
        );
    }

    private void toggleRightSidebar(Button collapseButton) {
        rightCollapsed = !rightCollapsed;
        collapseButton.setText(rightCollapsed ? "<" : ">");
        animateSidebarState(
                rightSidebar,
                rightSidebarTitle,
                settingsList,
                rightCollapsed,
                rightCollapsed ? COLLAPSED_WIDTH : RIGHT_EXPANDED_WIDTH
        );
    }

    private void animateSidebarState(VBox sidebar, Region title, Region body, boolean collapsing, double targetWidth) {
        if (collapsing) {
            ParallelTransition fadeOut = buildFade(title, body, 1, 0);
            fadeOut.setOnFinished(event -> {
                setNodeExpanded(title, false);
                setNodeExpanded(body, false);
                animateSidebarWidth(sidebar, targetWidth, null);
            });
            fadeOut.play();
            return;
        }

        setNodeExpanded(title, true);
        setNodeExpanded(body, true);
        title.setOpacity(0);
        body.setOpacity(0);
        animateSidebarWidth(sidebar, targetWidth, () -> buildFade(title, body, 0, 1).play());
    }

    private ParallelTransition buildFade(Region title, Region body, double fromValue, double toValue) {
        FadeTransition titleFade = new FadeTransition(TEXT_FADE_TIME, title);
        titleFade.setFromValue(fromValue);
        titleFade.setToValue(toValue);

        FadeTransition bodyFade = new FadeTransition(TEXT_FADE_TIME, body);
        bodyFade.setFromValue(fromValue);
        bodyFade.setToValue(toValue);

        return new ParallelTransition(titleFade, bodyFade);
    }

    private void setNodeExpanded(Region node, boolean expanded) {
        node.setVisible(expanded);
        node.setManaged(expanded);
    }

    private void animateSidebarWidth(VBox sidebar, double targetWidth, Runnable onFinished) {
        // JavaFX layout reads prefWidth during each pulse, so animating it keeps resizing smooth.
        Timeline animation = new Timeline(
                new KeyFrame(
                        PANEL_ANIMATION_TIME,
                        new KeyValue(sidebar.prefWidthProperty(), targetWidth, Interpolator.EASE_BOTH)
                )
        );
        if (onFinished != null) {
            animation.setOnFinished(event -> onFinished.run());
        }
        animation.play();
    }

    private void playFadeIn(StackPane root) {
        FadeTransition fade = new FadeTransition(Duration.millis(220), root);
        fade.setFromValue(0);
        fade.setToValue(1);
        fade.play();
    }
}
