module Utils exposing (withCmdNone)


withCmdNone : a -> ( a, Cmd b )
withCmdNone value =
    ( value, Cmd.none )
