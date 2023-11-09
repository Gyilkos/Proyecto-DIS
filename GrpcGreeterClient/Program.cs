using System.Threading.Tasks;
using Grpc.Net.Client;
using GrpcGreeterClient;

// The port number must match the port of the gRPC server.
using var channel = GrpcChannel.ForAddress("http://localhost:5068");

var client = new Greeter.GreeterClient(channel);
var reply = await client.SayHelloAsync(
    new HelloRequest { Name = "GreeterClient" });
Console.WriteLine("Greeting: " + reply.Message);

int num = 3;
int numSum = 4;

var reply2 = await client.CuadradoAsync(
    new CuadradoRequest { Numero = num});

Console.WriteLine("Cuadrado de " + num + " = " + reply2.Cuadrado);


var reply3 = await client.SumaAsync(
    new SumaRequest { Numero = numSum}
);
Console.WriteLine("La suma de " + numSum + " con si mismo es = " + reply3.Suma);


Console.WriteLine("Press any key to exit...");
Console.ReadKey();
