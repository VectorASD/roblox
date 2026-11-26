local Types = require(script.Parent.Parent.Types)

return function(Iris: Types.Internal, widgets: Types.WidgetUtility)
    local abstractImage = {
        hasState = false,
        hasChildren = false,
        Args = {
            ["Image"] = 1,
            ["Size"] = 2,
            ["Rect"] = 3,
            ["ScaleType"] = 4,
            ["ResampleMode"] = 5,
            ["TileSize"] = 6,
            ["SliceCenter"] = 7,
            ["SliceScale"] = 8,
        },
        Discard = function(thisWidget: Types.Image)
            thisWidget.Instance:Destroy()
        end,
    } :: Types.WidgetClass

    --stylua: ignore
    Iris.WidgetConstructor("Image", widgets.extend(abstractImage, {
            Events = {
                ["hovered"] = widgets.EVENTS.hover(function(thisWidget: Types.Widget)
                    return thisWidget.Instance
                end),
            },
            Generate = function(thisWidget: Types.Image)
                local Image = Instance.new("ImageLabel")
                Image.Name = "Iris_Image"
                Image.BackgroundTransparency = 1
                Image.BorderSizePixel = 0
                Image.ImageColor3 = Iris._config.ImageColor
                Image.ImageTransparency = Iris._config.ImageTransparency
                -- Image.LayoutOrder = thisWidget.ZIndex
                -- Iris теперь глобально пересчитывает это по порядку отрисовки

                widgets.applyFrameStyle(Image, true)

                return Image
            end,
            Update = function(thisWidget: Types.Image)
                local Image = thisWidget.Instance :: ImageLabel
    
                Image.Image = thisWidget.arguments.Image or widgets.ICONS.UNKNOWN_TEXTURE
                Image.Size = thisWidget.arguments.Size
                if thisWidget.arguments.ScaleType then
                    Image.ScaleType = thisWidget.arguments.ScaleType
                    if thisWidget.arguments.ScaleType == Enum.ScaleType.Tile and thisWidget.arguments.TileSize then
                        Image.TileSize = thisWidget.arguments.TileSize
                    elseif thisWidget.arguments.ScaleType == Enum.ScaleType.Slice then
                        if thisWidget.arguments.SliceCenter then
                            Image.SliceCenter = thisWidget.arguments.SliceCenter
                        end
                        if thisWidget.arguments.SliceScale then
                            Image.SliceScale = thisWidget.arguments.SliceScale
                        end
                    end
                end
    
                if thisWidget.arguments.Rect then
                    Image.ImageRectOffset = thisWidget.arguments.Rect.Min
                    Image.ImageRectSize = Vector2.new(thisWidget.arguments.Rect.Width, thisWidget.arguments.Rect.Height)
                end
    
                if thisWidget.arguments.ResampleMode then
                    Image.ResampleMode = thisWidget.arguments.ResampleMode
                end
            end,
        } :: Types.WidgetClass)
    )

    --stylua: ignore
    Iris.WidgetConstructor("ImageButton", widgets.extend(abstractImage, {
            Events = {
                ["clicked"] = widgets.EVENTS.click(function(thisWidget: Types.Widget)
                    return thisWidget.Instance
                end),
                ["rightClicked"] = widgets.EVENTS.rightClick(function(thisWidget: Types.Widget)
                    return thisWidget.Instance
                end),
                ["doubleClicked"] = widgets.EVENTS.doubleClick(function(thisWidget: Types.Widget)
                    return thisWidget.Instance
                end),
                ["ctrlClicked"] = widgets.EVENTS.ctrlClick(function(thisWidget: Types.Widget)
                    return thisWidget.Instance
                end),
                ["hovered"] = widgets.EVENTS.hover(function(thisWidget: Types.Widget)
                    return thisWidget.Instance
                end),
            },
            Generate = function(thisWidget: Types.ImageButton)
                local Button = Instance.new("ImageButton")
                Button.Name = "Iris_ImageButton"
                Button.AutomaticSize = Enum.AutomaticSize.XY
                Button.BackgroundColor3 = Iris._config.FrameBgColor
                Button.BackgroundTransparency = Iris._config.FrameBgTransparency
                Button.BorderSizePixel = 0
                Button.Image = ""
                Button.ImageTransparency = 1
                -- Button.LayoutOrder = thisWidget.ZIndex
                -- Iris теперь глобально пересчитывает это по порядку отрисовки
                Button.AutoButtonColor = false
                
                widgets.applyFrameStyle(Button, true)
                widgets.UIPadding(Button, Vector2.new(Iris._config.ImageBorderSize, Iris._config.ImageBorderSize))
                
                local Image = Instance.new("ImageLabel")
                Image.Name = "ImageLabel"
                Image.BackgroundTransparency = 1
                Image.BorderSizePixel = 0
                Image.ImageColor3 = Iris._config.ImageColor
                Image.ImageTransparency = Iris._config.ImageTransparency
                Image.Parent = Button

                widgets.applyInteractionHighlights("Background", Button, Button, {
                    Color = Iris._config.FrameBgColor,
                    Transparency = Iris._config.FrameBgTransparency,
                    HoveredColor = Iris._config.FrameBgHoveredColor,
                    HoveredTransparency = Iris._config.FrameBgHoveredTransparency,
                    ActiveColor = Iris._config.FrameBgActiveColor,
                    ActiveTransparency = Iris._config.FrameBgActiveTransparency,
                })

                return Button
            end,
            Update = function(thisWidget: Types.ImageButton)
                local Button = thisWidget.Instance :: TextButton
                local Image: ImageLabel = Button.ImageLabel
    
                Image.Image = thisWidget.arguments.Image or widgets.ICONS.UNKNOWN_TEXTURE
                Image.Size = thisWidget.arguments.Size
                if thisWidget.arguments.ScaleType then
                    Image.ScaleType = thisWidget.arguments.ScaleType
                    if thisWidget.arguments.ScaleType == Enum.ScaleType.Tile and thisWidget.arguments.TileSize then
                        Image.TileSize = thisWidget.arguments.TileSize
                    elseif thisWidget.arguments.ScaleType == Enum.ScaleType.Slice then
                        if thisWidget.arguments.SliceCenter then
                            Image.SliceCenter = thisWidget.arguments.SliceCenter
                        end
                        if thisWidget.arguments.SliceScale then
                            Image.SliceScale = thisWidget.arguments.SliceScale
                        end
                    end
                end
    
                if thisWidget.arguments.Rect then
                    Image.ImageRectOffset = thisWidget.arguments.Rect.Min
                    Image.ImageRectSize = Vector2.new(thisWidget.arguments.Rect.Width, thisWidget.arguments.Rect.Height)
                end
    
                if thisWidget.arguments.ResampleMode then
                    Image.ResampleMode = thisWidget.arguments.ResampleMode
                end
            end,
        } :: Types.WidgetClass)
    )
    
    --stylua: ignore
    Iris.WidgetConstructor("AssetTile", widgets.extend(abstractImage, {
        Events = {
            ["clicked"] = widgets.EVENTS.click(function(thisWidget: Types.Widget)
                return thisWidget.Instance
            end),
            ["rightClicked"] = widgets.EVENTS.rightClick(function(thisWidget: Types.Widget)
                return thisWidget.Instance
            end),
            ["doubleClicked"] = widgets.EVENTS.doubleClick(function(thisWidget: Types.Widget)
                return thisWidget.Instance
            end),
            ["ctrlClicked"] = widgets.EVENTS.ctrlClick(function(thisWidget: Types.Widget)
                return thisWidget.Instance
            end),
            ["hovered"] = widgets.EVENTS.hover(function(thisWidget: Types.Widget)
                return thisWidget.Instance
            end),
        },
        Generate = function(thisWidget: Types.ImageButton)
            local ASSET_TILE_COLORS = {
                Color               = Color3.fromRGB(0, 0, 0),
                Transparency        = 0.15,
                HoveredColor        = Color3.fromRGB(33, 33, 33),
                HoveredTransparency = 0.05,
                ActiveColor         = Color3.fromRGB(33, 58, 84),
                ActiveTransparency  = 0,
            }

            local Button = Instance.new("ImageButton")
            Button.Name = "Iris_AssetTile"
            Button.BackgroundColor3       = ASSET_TILE_COLORS.Color
            Button.BackgroundTransparency = ASSET_TILE_COLORS.Transparency
            Button.BorderSizePixel = 0
            Button.Image = ""
            Button.ImageTransparency = 1
            Button.Size = UDim2.fromOffset(100, 100)
            -- Button.LayoutOrder = thisWidget.ZIndex
            -- Iris теперь глобально пересчитывает это по порядку отрисовки
            Button.AutoButtonColor = false
            Button.ScaleType = Enum.ScaleType.Fit

            widgets.applyFrameStyle(Button, true)
            if Iris._config.FrameRounding > 0 then
                widgets.UICorner(Button, Iris._config.FrameRounding)
            end

            local Image = Instance.new("ImageLabel")
            Image.Name = "ImageLabel"
            Image.BackgroundTransparency = 1
            Image.BorderSizePixel = 0
            Image.ImageColor3 = Iris._config.ImageColor
            Image.ImageTransparency = Iris._config.ImageTransparency
            Image.Size = UDim2.fromScale(1, 1)
            Image.ScaleType = Enum.ScaleType.Fit
            Image.Parent = Button

            -- Заготовка под будущие hover-кнопки (корзина, «надеть», описание).
            -- Пока пустая и невидимая; логика появится в следующих итерациях.
            local HoverOverlay = Instance.new("Frame")
            HoverOverlay.Name = "HoverOverlay"
            HoverOverlay.BackgroundColor3 = Color3.new(0, 0, 0)
            HoverOverlay.BackgroundTransparency = 1
            HoverOverlay.BorderSizePixel = 0
            HoverOverlay.Size = UDim2.fromScale(1, 1)
            HoverOverlay.Visible = false
            HoverOverlay.Parent = Button

            widgets.applyInteractionHighlights("Background", Button, Button, ASSET_TILE_COLORS)

            return Button
        end,
        Update = function(thisWidget: Types.ImageButton)
            local Button = thisWidget.Instance :: ImageButton
            local Image: ImageLabel = Button.ImageLabel

            Button.Size = thisWidget.arguments.Size or UDim2.fromOffset(150, 150)

            local imgArg = thisWidget.arguments.Image
            if type(imgArg) == "number" then
                -- Determine thumb resolution based on Size argument
                local thumbSize = 150
                local sizeArg = thisWidget.arguments.Size
                if sizeArg and sizeArg.X.Scale == 0 and sizeArg.Y.Scale == 0 then
                    if math.max(sizeArg.X.Offset, sizeArg.Y.Offset) > 150 then
                        thumbSize = 420
                    end
                else
                    -- Scale-based size — use actual rendered size (may be 0 on first frame)
                    local abs = Button.AbsoluteSize
                    if math.max(abs.X, abs.Y) > 150 then
                        thumbSize = 420
                    end
                end
                Image.Image = string.format("rbxthumb://type=Asset&id=%d&w=%d&h=%d", imgArg, thumbSize, thumbSize)
            elseif type(imgArg) == "string" and imgArg ~= "" then
                -- на случай, если кто-то передал готовый URL (для дебага/кастомных превью)
                Image.Image = imgArg
            else
                Image.Image = widgets.ICONS.UNKNOWN_TEXTURE
            end

            if thisWidget.arguments.ScaleType then
                Image.ScaleType = thisWidget.arguments.ScaleType
            end

            if thisWidget.arguments.Rect then
                Image.ImageRectOffset = thisWidget.arguments.Rect.Min
                Image.ImageRectSize = Vector2.new(thisWidget.arguments.Rect.Width, thisWidget.arguments.Rect.Height)
            end

            if thisWidget.arguments.ResampleMode then
                Image.ResampleMode = thisWidget.arguments.ResampleMode
            end
        end,
    } :: Types.WidgetClass))
end
