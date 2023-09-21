module master_slave(
  input J,K,clk,pr,clr,
  output reg Q,Qbar
);
  wire w1,w2,w3,w4;
  always@(clk) begin
    if(pr) begin
      Q<=1;
      Qbar<=0;
    end
    else if(clr) begin
      Q<=0;
      Qbar<=1;
    end
    else begin
      w1 <= ~(J & clk & Qbar);
      w2 <= ~(K & clk & Q);
      w3 <= ~(Qmbar & w1);
      w4 <= ~(Qm & w2);
      w5 <= ~(w3 & (~clk));
      w6 <= ~(w4 & (~clk));
      Q <= ~(Qbar & pr & w5);
      Qbar <= ~(Qbar & clr & w6);
    end
  end
endmodule
    
