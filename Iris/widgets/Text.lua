local Types = require(script.Parent.Parent.Types)

return function(Iris: Types.Internal, widgets: Types.WidgetUtility)
    --stylua: ignore
    Iris.WidgetConstructor("Text", {
        hasState = false,
        hasChildren = false,
        Args = {
            ["Text"] = 1,
            ["Wrapped"] = 2,
            ["Color"] = 3,
            ["RichText"] = 4,
            ["Copyable"] = 5,
        },
        Events = {
            ["hovered"] = widgets.EVENTS.hover(function(thisWidget: Types.Widget)
                return thisWidget.Instance
            end),
        },
        Generate = function(thisWidget: Types.Text)
            local Box = Instance.new("TextBox")
            Box.Name = "Iris_Text"
            Box.TextEditable     = false  -- запрет ввода
            Box.ClearTextOnFocus = false  -- текст не исчезает при клике
            Box.TextTruncate     = Enum.TextTruncate.None  -- как у TextLabel
            Box.AutomaticSize    = Enum.AutomaticSize.XY
            Box.Size             = UDim2.fromOffset(0, 0)
            Box.BackgroundTransparency = 1
            Box.BorderSizePixel = 0

            widgets.applyTextStyle(Box)
            widgets.UIPadding(Box, Vector2.new(0, 2))

            return Box
        end,
        Update = function(thisWidget: Types.Text)
            local Box = thisWidget.Instance :: TextBox
            local args = thisWidget.arguments

            if args.Text == nil then
                error("Text argument is required for Iris.Text().", 5)
            end

            -- Copyable: toggle focusability. TextEditable всегда false,
            -- чтобы даже при фокусе нельзя было изменить текст
            local copyable = args.Copyable == true
            Box.TextEditable = false
            Box.Active       = copyable
            Box.Selectable   = copyable

            -- Если Copyable только что переключили false → true → false,
            -- а фокус уже стоял - принудительно снимаем
            if not copyable and Box:IsFocused() then
                Box:ReleaseFocus()
            end

            if args.Wrapped ~= nil then
                Box.TextWrapped = args.Wrapped
            else
                Box.TextWrapped = Iris._config.TextWrapped
            end
            if args.Color then
                Box.TextColor3 = args.Color
            else
                Box.TextColor3 = Iris._config.TextColor
            end
            if args.RichText ~= nil then
                Box.RichText = args.RichText
            else
                Box.RichText = Iris._config.RichText
            end

            Box.Text = args.Text
        end,
        Discard = function(thisWidget: Types.Text)
            thisWidget.Instance:Destroy()
        end,
    } :: Types.WidgetClass)

    --stylua: ignore
    Iris.WidgetConstructor("SeparatorText", {
        hasState = false,
        hasChildren = false,
        Args = {
            ["Text"] = 1,
        },
        Events = {
            ["hovered"] = widgets.EVENTS.hover(function(thisWidget: Types.Widget)
                return thisWidget.Instance
            end),
        },
        Generate = function(_thisWidget: Types.SeparatorText)
            local SeparatorText = Instance.new("Frame")
            SeparatorText.Name = "Iris_SeparatorText"
            SeparatorText.AutomaticSize = Enum.AutomaticSize.Y
            SeparatorText.Size = UDim2.new(Iris._config.ItemWidth, UDim.new())
            SeparatorText.BackgroundTransparency = 1
            SeparatorText.BorderSizePixel = 0
            SeparatorText.ClipsDescendants = true

            widgets.UIPadding(SeparatorText, Vector2.new(0, Iris._config.SeparatorTextPadding.Y))
            widgets.UIListLayout(SeparatorText, Enum.FillDirection.Horizontal, UDim.new(0, Iris._config.ItemSpacing.X))

            SeparatorText.UIListLayout.VerticalAlignment = Enum.VerticalAlignment.Center

            local TextLabel = Instance.new("TextLabel")
            TextLabel.Name = "TextLabel"
            TextLabel.AutomaticSize = Enum.AutomaticSize.XY
            TextLabel.BackgroundTransparency = 1
            TextLabel.BorderSizePixel = 0
            TextLabel.LayoutOrder = 1

            widgets.applyTextStyle(TextLabel)

            TextLabel.Parent = SeparatorText

            local Left = Instance.new("Frame")
            Left.Name = "Left"
            Left.AnchorPoint = Vector2.new(1, 0.5)
            Left.Size = UDim2.fromOffset(Iris._config.SeparatorTextPadding.X - Iris._config.ItemSpacing.X, Iris._config.SeparatorTextBorderSize)
            Left.BackgroundColor3 = Iris._config.SeparatorColor
            Left.BackgroundTransparency = Iris._config.SeparatorTransparency
            Left.BorderSizePixel = 0

            Left.Parent = SeparatorText

            local Right = Instance.new("Frame")
            Right.Name = "Right"
            Right.AnchorPoint = Vector2.new(1, 0.5)
            Right.Size = UDim2.new(1, 0, 0, Iris._config.SeparatorTextBorderSize)
            Right.BackgroundColor3 = Iris._config.SeparatorColor
            Right.BackgroundTransparency = Iris._config.SeparatorTransparency
            Right.BorderSizePixel = 0
            Right.LayoutOrder = 2

            Right.Parent = SeparatorText

            return SeparatorText
        end,
        Update = function(thisWidget: Types.SeparatorText)
            local SeparatorText = thisWidget.Instance :: Frame
            local TextLabel: TextLabel = SeparatorText.TextLabel
            if thisWidget.arguments.Text == nil then
                error("Text argument is required for Iris.SeparatorText().", 5)
            end
            TextLabel.Text = thisWidget.arguments.Text
        end,
        Discard = function(thisWidget: Types.SeparatorText)
            thisWidget.Instance:Destroy()
        end,
    } :: Types.WidgetClass)
end
