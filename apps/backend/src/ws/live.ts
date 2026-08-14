export async function academyRealtime(socket: any) {
  socket.send(
    JSON.stringify({
      type: "academy.live",
      students: 14482,
    }),
  );
}
