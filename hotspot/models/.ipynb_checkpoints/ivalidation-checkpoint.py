from hotspot.models import idraw, iticket


class iValidation:
    _draw_id = 0;
    _draw_bin_0140 = 0;
    _draw_bin_4180 = 0;

    def __init__(self, drawID):
        self._draw_id = drawID;
        dr = idraw.iDraw(self._draw_id);
        dr.setup();
        self._draw_bin_0140 = dr.d_bin0140
        self._draw_bin_4180 = dr.d_bin4180

        pass;
    
    def validate(self, ticketID):
        tk = iticket.iTicket(ticketID)
        tk.setup();
        match0180 = 0
        pass;
    
    def get_bin0140(self):
        return self._draw_bin_0140

    def get_bin4180(self):
        return self._draw_bin_4180