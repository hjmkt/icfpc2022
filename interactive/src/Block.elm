module Block exposing (Block(..), BlockDict, Move, Rect, Rgba, applyColor, applyCutHLine, applyCutPoint, applyCutVLine)

import Dict exposing (Dict)


type alias Rect =
    { x : Int
    , y : Int
    , w : Int
    , h : Int
    }


type alias Rgba =
    { r : Int
    , g : Int
    , b : Int
    , a : Int
    }


type Block
    = SimpleBlock Rect Rgba


type alias BlockDict =
    Dict String Block


type Move
    = CutVLine String Int
    | CutHLine String Int
    | CutPoint String Int Int
    | Color String Int Int Int Int


applyColor : String -> Int -> Int -> Int -> Int -> BlockDict -> BlockDict
applyColor id r g b a =
    Dict.update id <|
        Maybe.map <|
            \block ->
                case block of
                    SimpleBlock rect _ ->
                        SimpleBlock rect { r = r, g = g, b = b, a = a }


applyCutVLine : String -> Int -> BlockDict -> BlockDict
applyCutVLine id xPos blockDict =
    case Dict.get id blockDict of
        Nothing ->
            -- ブロックがない
            blockDict

        Just (SimpleBlock { x, y, w, h } color) ->
            if xPos > x && xPos <= x + w then
                let
                    removedBlockDict =
                        Dict.remove id blockDict

                    leftId =
                        id ++ ".0"

                    leftW =
                        xPos - x

                    left =
                        SimpleBlock { x = x, y = y, w = leftW, h = h } color

                    rightId =
                        id ++ ".1"

                    rightW =
                        w - leftW

                    right =
                        SimpleBlock { x = xPos, y = y, w = rightW, h = h } color
                in
                Dict.insert leftId left <|
                    Dict.insert rightId right removedBlockDict

            else
                -- 範囲外
                blockDict


applyCutHLine : String -> Int -> BlockDict -> BlockDict
applyCutHLine id yPos blockDict =
    case Dict.get id blockDict of
        Nothing ->
            -- ブロックがない
            blockDict

        Just (SimpleBlock { x, y, w, h } color) ->
            if yPos > y && yPos <= y + h then
                let
                    removedBlockDict =
                        Dict.remove id blockDict

                    downId =
                        id ++ ".0"

                    downH =
                        yPos - y

                    down =
                        SimpleBlock { x = x, y = y, w = w, h = downH } color

                    upId =
                        id ++ ".1"

                    upH =
                        h - downH

                    up =
                        SimpleBlock { x = x, y = yPos, w = w, h = upH } color
                in
                Dict.insert downId down <|
                    Dict.insert upId up removedBlockDict

            else
                -- 範囲外
                blockDict


applyCutPoint : String -> Int -> Int -> BlockDict -> BlockDict
applyCutPoint id xPos yPos blockDict =
    case Dict.get id blockDict of
        Nothing ->
            -- ブロックがない
            blockDict

        Just (SimpleBlock { x, y, w, h } color) ->
            if xPos > x && xPos <= x + w && yPos > y && yPos <= y + h then
                let
                    removedBlockDict =
                        Dict.remove id blockDict

                    leftW =
                        xPos - x

                    rightW =
                        w - leftW

                    downH =
                        yPos - y

                    upH =
                        h - downH

                    leftDownId =
                        id ++ ".0"

                    leftDown =
                        SimpleBlock { x = x, y = y, w = leftW, h = downH } color

                    rightDownId =
                        id ++ ".1"

                    rightDown =
                        SimpleBlock { x = xPos, y = y, w = rightW, h = downH } color

                    rightUpId =
                        id ++ ".2"

                    rightUp =
                        SimpleBlock { x = xPos, y = yPos, w = rightW, h = upH } color

                    leftUpId =
                        id ++ ".3"

                    leftUp =
                        SimpleBlock { x = x, y = yPos, w = leftW, h = upH } color
                in
                Dict.insert leftDownId leftDown <|
                    Dict.insert rightDownId rightDown <|
                        Dict.insert rightUpId rightUp <|
                            Dict.insert leftUpId leftUp removedBlockDict

            else
                -- 範囲外
                blockDict
