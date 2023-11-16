using Grpc.Core;
using servicio;
using System.Data.SQLite;

namespace servicio.Services;

public class GreeterService : Greeter.GreeterBase
{
    private readonly ILogger<GreeterService> _logger;
    public GreeterService(ILogger<GreeterService> logger)
    {
        _logger = logger;
    }
    

    public override Task<HelloReply> SayHello(HelloRequest request, ServerCallContext context)
    {
        return Task.FromResult(new HelloReply
        {
            Message = "Hello " + request.Name
        });
    }

    public override Task<CuadradoReply> Cuadrado(CuadradoRequest request, ServerCallContext context)
    {
        return Task.FromResult(new CuadradoReply { Cuadrado = request.Numero*request.Numero});
    }

     //falta ver el te ma de las variables de las cuales dan error
    

    // public override Task<PatenteReply> Patente(PatenteRequest request, ServerCallContext context)
    // {
    //      // Supongamos que esta función busca el estado de la patente
    //      string estadoPatente = BuscarEstadoPatente(request.NumeroPatente);

    //      return Task.FromResult(new PatenteReply { EstadoPatente = estadoPatente });
    // }

    private string BuscarEstadoPatente(string numeroPatente)
    {
        string estadoPatente = null;
        string connectionString = "Data Source=DBcamioneta.db;Version=3;";
        using (SQLiteConnection connection = new SQLiteConnection(connectionString))
        {
            connection.Open();

            string sql = "SELECT Estado FROM Camioneta WHERE Patente = @NumeroPatente";
            using (SQLiteCommand command = new SQLiteCommand(sql, connection))
            {
                command.Parameters.AddWithValue("@NumeroPatente", numeroPatente);

                using (SQLiteDataReader reader = command.ExecuteReader())
                {
                    if (reader.Read())
                    {
                        estadoPatente = reader["Estado"].ToString();
                    }
                }
            }
        }

        return estadoPatente;
    }
   
}
