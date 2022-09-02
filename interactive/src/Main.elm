port module Main exposing (main)

import Block exposing (Block(..), BlockDict, Move, Rgba, applyColor, applyCutHLine, applyCutPoint, applyCutVLine)
import Browser exposing (Document)
import Dict exposing (Dict)
import Element exposing (Element)
import Element.Background as Background
import Element.Border as Border
import Element.Events as Events
import Element.Input as Input
import Json.Decode as Dec
import Json.Encode as Enc
import Utils exposing (withCmdNone)



-- PORT


port jsToElm : (Dec.Value -> msg) -> Sub msg


port elmToJs : Enc.Value -> Cmd msg



-- MAIN


main : Program Flags Model Msg
main =
    Browser.document
        { init = init
        , update = update
        , view = view
        , subscriptions = subscriptions
        }



-- MODEL


type alias Flags =
    { winWidth : Float
    , winHeight : Float
    }


type alias Model =
    { canvasWidth : Int
    , canvasHeight : Int
    , moveList : List Move
    , blockDict : BlockDict
    , tool : Tool
    , curColor : Rgba
    , curX : Int
    , curY : Int
    , curBlock : String
    }


type Tool
    = ToolCutH
    | ToolCutV
    | ToolCutPoint
    | ToolColor


init : Flags -> ( Model, Cmd Msg )
init _ =
    let
        canvasWidth =
            400

        canvasHeight =
            400
    in
    withCmdNone
        { canvasWidth = canvasWidth
        , canvasHeight = canvasHeight
        , moveList = []
        , blockDict =
            Dict.singleton "0" <|
                SimpleBlock
                    { x = 0, y = 0, w = canvasWidth - 1, h = canvasHeight - 1 }
                    { r = 255, g = 255, b = 255, a = 255 }
        , tool = ToolColor
        , curColor = { r = 0, g = 0, b = 0, a = 255 }
        , curX = 100
        , curY = 100
        , curBlock = "0"
        }



-- UPDATE


type Msg
    = ToolChanged Tool
    | ColorChanged ColorElem String
    | ChangeBlock String
    | CurXChanged String
    | CurYChanged String
    | OnApply


type ColorElem
    = Red
    | Green
    | Blue
    | Alpha


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        ToolChanged tool ->
            withCmdNone { model | tool = tool }

        ColorChanged elem str ->
            let
                curColor =
                    model.curColor

                value =
                    clamp 0 255 <|
                        Maybe.withDefault 255 (String.toInt str)
            in
            case elem of
                Red ->
                    withCmdNone { model | curColor = { curColor | r = value } }

                Green ->
                    withCmdNone { model | curColor = { curColor | g = value } }

                Blue ->
                    withCmdNone { model | curColor = { curColor | b = value } }

                Alpha ->
                    withCmdNone { model | curColor = { curColor | a = value } }

        ChangeBlock id ->
            withCmdNone { model | curBlock = id }

        CurXChanged str ->
            let
                value =
                    clamp 0 399 <|
                        Maybe.withDefault 0 (String.toInt str)
            in
            withCmdNone { model | curX = value }

        CurYChanged str ->
            let
                value =
                    clamp 0 399 <|
                        Maybe.withDefault 0 (String.toInt str)
            in
            withCmdNone { model | curY = value }

        OnApply ->
            case model.tool of
                ToolColor ->
                    withCmdNone
                        { model
                            | blockDict =
                                applyColor
                                    model.curBlock
                                    model.curColor.r
                                    model.curColor.g
                                    model.curColor.b
                                    model.curColor.a
                                    model.blockDict
                        }

                ToolCutH ->
                    withCmdNone
                        { model
                            | blockDict = applyCutHLine model.curBlock model.curY model.blockDict
                        }

                ToolCutV ->
                    withCmdNone
                        { model
                            | blockDict = applyCutVLine model.curBlock model.curX model.blockDict
                        }

                ToolCutPoint ->
                    withCmdNone
                        { model
                            | blockDict = applyCutPoint model.curBlock model.curX model.curY model.blockDict
                        }



-- VIEW


view : Model -> Document Msg
view model =
    { title = "Visualizer"
    , body =
        [ Element.layout [ Element.padding 20 ] <|
            Element.column []
                [ Element.row [ Element.spacing 20 ]
                    [ canvasElement model
                    , Element.image []
                        { src = "1.png", description = "1.png" }
                    ]
                , toolAreaElement model
                ]
        ]
    }


canvasElement : Model -> Element Msg
canvasElement model =
    let
        blockElements =
            Dict.foldl (\id block list -> Element.inFront (blockElement model id block) :: list) [] model.blockDict
    in
    Element.el
        ([ Element.width (Element.px model.canvasWidth)
         , Element.height (Element.px model.canvasHeight)
         ]
            ++ blockElements
            ++ [ Element.inFront (hlineElement model), Element.inFront (vlineElement model) ]
        )
        Element.none


blockElement : Model -> String -> Block -> Element Msg
blockElement model id block =
    case block of
        SimpleBlock { x, y, w, h } { r, g, b, a } ->
            Element.el
                [ Element.moveRight (toFloat x)
                , Element.moveUp (toFloat (y - model.canvasHeight + h))
                , Element.width (Element.px w)
                , Element.height (Element.px h)
                , Background.color (Element.rgba255 r g b (toFloat a / 255))
                , Events.onClick (ChangeBlock id)
                ]
                Element.none


hlineElement : Model -> Element Msg
hlineElement model =
    if model.tool == ToolCutH || model.tool == ToolCutPoint then
        Element.el
            [ Element.width (Element.px model.canvasWidth)
            , Element.height (Element.px 1)
            , Element.moveUp (toFloat (model.curY - model.canvasHeight) + 0.5)
            , Background.color (Element.rgba 255 0 0 255)
            ]
            Element.none

    else
        Element.none


vlineElement : Model -> Element Msg
vlineElement model =
    if model.tool == ToolCutV || model.tool == ToolCutPoint then
        Element.el
            [ Element.width (Element.px 1)
            , Element.height (Element.px model.canvasHeight)
            , Element.moveRight (toFloat model.curX + 0.5)
            , Background.color (Element.rgba 255 0 0 255)
            ]
            Element.none

    else
        Element.none


toolAreaElement : Model -> Element Msg
toolAreaElement model =
    Element.row
        [ Element.paddingXY 0 10 ]
        [ toolSelectorElement model
        ]


toolSelectorElement : Model -> Element Msg
toolSelectorElement model =
    Element.row [ Element.spacing 30 ] <|
        [ Element.column [ Element.alignTop ]
            [ Element.text <| "curBlock = " ++ model.curBlock
            , Input.radio []
                { onChange = ToolChanged
                , selected = Just model.tool
                , label = Input.labelAbove [] (Element.text "move type")
                , options =
                    [ Input.option ToolColor (Element.text "color")
                    , Input.option ToolCutV (Element.text "cut x")
                    , Input.option ToolCutH (Element.text "cut y")
                    , Input.option ToolCutPoint (Element.text "cut")
                    ]
                }
            ]
        ]
            ++ (case model.tool of
                    ToolColor ->
                        [ toolColorElement model ]

                    ToolCutH ->
                        [ toolCutYElement model ]

                    ToolCutV ->
                        [ toolCutXElement model ]

                    ToolCutPoint ->
                        [ toolCutXElement model, toolCutYElement model ]
               )
            ++ [ Input.button [ Element.padding 10, Border.width 2, Border.color (Element.rgb255 0 0 0) ] { onPress = Just OnApply, label = Element.text "APPLY" } ]


toolColorElement : Model -> Element Msg
toolColorElement model =
    Element.column [ Element.width (Element.px 100) ]
        [ Input.text []
            { onChange = ColorChanged Red
            , text = String.fromInt model.curColor.r
            , placeholder = Nothing
            , label = Input.labelLeft [] (Element.text "R")
            }
        , Input.text []
            { onChange = ColorChanged Green
            , text = String.fromInt model.curColor.g
            , placeholder = Nothing
            , label = Input.labelLeft [] (Element.text "G")
            }
        , Input.text []
            { onChange = ColorChanged Blue
            , text = String.fromInt model.curColor.b
            , placeholder = Nothing
            , label = Input.labelLeft [] (Element.text "B")
            }
        , Input.text []
            { onChange = ColorChanged Alpha
            , text = String.fromInt model.curColor.a
            , placeholder = Nothing
            , label = Input.labelLeft [] (Element.text "A")
            }
        , Element.el
            [ Element.height (Element.px 30)
            , Element.width (Element.px 100)
            , Background.color
                (Element.rgba255
                    model.curColor.r
                    model.curColor.g
                    model.curColor.b
                    (toFloat model.curColor.a / 255)
                )
            ]
            Element.none
        ]


toolCutXElement : Model -> Element Msg
toolCutXElement model =
    Element.column [ Element.width (Element.px 100) ]
        [ Input.text []
            { onChange = CurXChanged
            , text = String.fromInt model.curX
            , placeholder = Nothing
            , label = Input.labelLeft [] (Element.text "X")
            }
        ]


toolCutYElement : Model -> Element Msg
toolCutYElement model =
    Element.column [ Element.width (Element.px 100) ]
        [ Input.text []
            { onChange = CurYChanged
            , text = String.fromInt model.curY
            , placeholder = Nothing
            , label = Input.labelLeft [] (Element.text "Y")
            }
        ]
