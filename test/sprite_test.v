`default_nettype none
module top(
    input clock_in,
    output LED0, LED1, LED2,
    output lcd_clk,
    output [7:0] lcd_dat,
    output lcd_hsync,
    output lcd_vsync,
    output lcd_den,
    output lcd_reset);

wire pixclk;
wire locked;
pll pll_i(.clock_in(clock_in), .clock_out(pixclk), .locked(locked));


wire [11:0] sprite_x, sprite_y;
wire [23:0] rgb_data;

lcd_ctrl lcddrv_i (.clk(pixclk), //19.2MHz pixel clock in
                  .resetn(locked),
                  .sprite_x(sprite_x),
                  .sprite_y(sprite_y),
                  .rgb_data(rgb_data),
                  .lcd_dat(lcd_dat),
                  .lcd_hsync(lcd_hsync),
                  .lcd_vsync(lcd_vsync),
                  .lcd_den(lcd_den));

localparam ctr_width = 26;

reg [ctr_width-1:0] ctr = 0;

always@(posedge pixclk)
  ctr <= ctr + 1;

wire [11:0] spen;

wire [1:0] ctrtop = ctr[ctr_width-1:ctr_width-2];

assign spen = (ctrtop == 1) ? 12'b100_000_001_001 :
              (ctrtop == 2) ? 12'b000_100_000_010 :
              (ctrtop == 3) ? 12'b001_000_100_100 :
              12'b000_001_000_010;

wire [1:0] spdat;

sprites sp_i(
	.clock(pixclk),
  .reset(1'b0),
	.vx(sprite_x),
	.vy(sprite_y),
	.enables(spen),
	.pixel(spdat));

assign rgb_data = (spdat == 1) ? 24'hFF0000 :
                  (spdat == 2) ? 24'h00FF00 :
                  (spdat == 3) ? 24'h0000FF :
                  24'hFFFFFF;

assign LED0 = locked;
assign LED1 = spen[1];
assign LED2 = spen[2];

assign lcd_clk = pixclk;

assign lcd_reset = 1'b1;

endmodule
